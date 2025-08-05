class SessionDomain:
    """
    domain for session-related business logic
    handles session creation and validation with user authorization checks
    """
    
    def __init__(self, session_repository, application_repository, jwt_service):
        """
        initialize session domain
        
        args:
            session_repository: instance of SessionRepository
            application_repository: instance of ApplicationRepository  
            jwt_service: instance of JWTService
        """
        self.session_repository = session_repository
        self.application_repository = application_repository
        self.jwt_service = jwt_service
    
    def initialize_session(self, cognito_tokens, application_id, device_info=None):
        """
        initialize a new session with cognito tokens
        validates user authorization for the application first
        
        args:
            cognito_tokens (dict): tokens from cognito
            application_id (str): the application requesting session
            device_info (dict): optional device information (user_agent, ip_address, etc.)
        
        returns:
            str: session_id if successful
        
        raises:
            ValueError: if user not authorized or invalid tokens
        """
        # validate the id token and extract user info
        id_token = cognito_tokens.get('id_token')
        if not id_token:
            raise ValueError("missing id_token in cognito tokens")
        
        try:
            user_info = self.jwt_service.extract_user_info(id_token)
            cognito_sub = user_info['sub']
        except ValueError as e:
            raise ValueError(f"invalid id_token: {str(e)}")
        
        # find user by cognito sub
        user = self.application_repository.find_user_by_sub(cognito_sub)
        
        # If user not found, create a new user using the Cognito attributes
        if not user:
            print(f"User not found with sub: {cognito_sub}. Creating new user from Cognito attributes.")
            from services.repositories.user_repository import UserRepository
            user_repository = UserRepository(self.application_repository.dynamodb_service)
            
            # Extract attributes from JWT token
            cognito_attributes = {
                'sub': cognito_sub,
                'email': user_info.get('email', ''),
                'name': user_info.get('name', ''),
                'phone_number': user_info.get('phone_number', ''),
                'gender': user_info.get('gender', ''),
                'custom:accepts_marketing': user_info.get('custom:accepts_marketing', 'false')
            }
            
            # Create the user
            user_id, user = user_repository.create_user(cognito_attributes)
            print(f"Created new user with ID: {user_id}")
            
            # Create application-user relationship (authorize user for the application)
            self.application_repository.create_app_user_relationship(application_id, user_id)
            print(f"Authorized user {user_id} for application {application_id}")
        else:
            user_id = user['PK']  # extract user_id
            
            # Check if user is authorized for this application (jambyref.md simple schema)
            is_authorized = self.application_repository.check_app_user_authorization(application_id, user_id)
            if not is_authorized:
                # If not authorized, create the authorization
                self.application_repository.create_app_user_relationship(application_id, user_id)
                print(f"Authorized user {user_id} for application {application_id}")
        
        # create the session with tokens and device info
        session_id = self.session_repository.create_session(user_id, cognito_tokens, application_id, device_info)
        
        return session_id
    
    def get_session_tokens(self, session_id):
        """
        get tokens for a session
        
        args:
            session_id (str): the session id
            
        returns:
            dict: session data with tokens, or none if not found/expired
        """
        from datetime import datetime, timedelta
        import os
        from services.aws.cognito_user_service import CognitoUserService
        
        # Get the session data
        session = self.session_repository.get_session(session_id)
        
        if not session:
            return None
            
        # Check if access token is expired or will expire soon (within 5 minutes)
        try:
            # If we have an expires_at field, use that to check expiration
            expires_at = session.get('expires_at')
            if expires_at:
                expiry_time = datetime.fromisoformat(expires_at)
                # If token expires within 5 minutes or is already expired
                if datetime.now() + timedelta(minutes=5) > expiry_time:
                    print(f"Access token for session {session_id} is expired or expiring soon. Attempting to refresh...")
                    
                    # Check if we have a refresh token
                    refresh_token = session.get('refresh_token')
                    if not refresh_token:
                        print(f"No refresh token available for session {session_id}")
                        return None
                    
                    # Initialize CognitoUserService if not already available
                    cognito_service = CognitoUserService()
                    
                    try:
                        # Refresh the tokens
                        new_tokens = cognito_service.refresh_tokens(refresh_token)
                        
                        if new_tokens and new_tokens.get('access_token') and new_tokens.get('id_token'):
                            # Calculate new expiration time (1 hour from now)
                            new_expires_at = (datetime.now() + timedelta(hours=1)).isoformat()
                            
                            # Update session with new tokens
                            session.update({
                                'id_token': new_tokens.get('id_token'),
                                'access_token': new_tokens.get('access_token'),
                                'refresh_token': new_tokens.get('refresh_token', refresh_token),
                                'expires_at': new_expires_at
                            })
                            
                            # Update the session in DynamoDB
                            self.session_repository.update_session_tokens(session_id, new_tokens, new_expires_at)
                            
                            print(f"Successfully refreshed tokens for session {session_id}")
                        else:
                            print(f"Failed to refresh tokens for session {session_id}: Invalid token response")
                    except Exception as e:
                        print(f"Error refreshing tokens for session {session_id}: {str(e)}")
                        # If refresh fails, return the session anyway - let the client handle token issues
        except Exception as e:
            print(f"Error checking token expiration for session {session_id}: {str(e)}")
        
        return session
    
    def get_user_sessions(self, user_id, include_expired=False):
        """
        get all sessions for a user with additional info
        
        args:
            user_id (str): the user id
            include_expired (bool): whether to include expired sessions
            
        returns:
            dict: sessions with enriched data
        """
        sessions_data = self.session_repository.get_user_sessions(user_id, include_expired)
        
        # enrich session data with additional info if needed
        for session_list in [sessions_data['active'], sessions_data['expired']]:
            for session in session_list:
                # extract device info from tokens if available
                session['session_id'] = session['PK']
                session['device_info'] = self._extract_device_info(session)
                session['location_info'] = self._extract_location_info(session)
        
        return sessions_data
    
    def revoke_session(self, session_id, requesting_user_id):
        """
        revoke a specific session with authorization check
        
        args:
            session_id (str): the session to revoke
            requesting_user_id (str): user requesting revocation
            
        returns:
            bool: success status
            
        raises:
            ValueError: if unauthorized or session not found
        """
        # get session to verify ownership
        session = self.session_repository.get_session(session_id)
        if not session:
            raise ValueError("session not found")
        
        # verify user owns this session
        if session.get('user_id') != requesting_user_id:
            raise ValueError("unauthorized to revoke this session")
        
        # revoke the session
        self.session_repository.delete_session(session_id)
        return True
    
    def revoke_all_other_sessions(self, user_id, current_session_id):
        """
        revoke all other sessions for a user (keep current one)
        
        args:
            user_id (str): the user id
            current_session_id (str): current session to keep
            
        returns:
            int: number of sessions revoked
        """
        return self.session_repository.revoke_all_user_sessions(user_id, current_session_id)
    
    def _extract_device_info(self, session):
        """
        extract device info from session data
        parses user-agent if available
        """
        # Check if we already have device_info in the session
        if 'device_info' in session and isinstance(session['device_info'], dict):
            # Return the stored device_info with any additional parsing
            stored_device_info = session['device_info']
            
            # Start with basic info - no IP address for security
            result = {}
            
            # Try to parse user agent if available
            user_agent = stored_device_info.get('user_agent') or session.get('user_agent')
            if user_agent:
                # Basic parsing of user agent
                browser = 'Unknown'
                os = 'Unknown'
                device = 'Unknown'
                
                # Very simple user agent parsing - in production you'd use a proper library
                user_agent = user_agent.lower()
                
                # Detect browser
                if 'firefox' in user_agent:
                    browser = 'Firefox'
                elif 'chrome' in user_agent and 'edg' not in user_agent:
                    browser = 'Chrome'
                elif 'safari' in user_agent and 'chrome' not in user_agent:
                    browser = 'Safari'
                elif 'edg' in user_agent:
                    browser = 'Edge'
                elif 'opera' in user_agent or 'opr' in user_agent:
                    browser = 'Opera'
                
                # Detect OS
                if 'windows' in user_agent:
                    os = 'Windows'
                elif 'macintosh' in user_agent or 'mac os' in user_agent:
                    os = 'macOS'
                elif 'linux' in user_agent:
                    os = 'Linux'
                elif 'android' in user_agent:
                    os = 'Android'
                elif 'iphone' in user_agent or 'ipad' in user_agent:
                    os = 'iOS'
                
                # Detect device type
                if 'mobile' in user_agent or 'android' in user_agent or 'iphone' in user_agent:
                    device = 'Mobile'
                elif 'tablet' in user_agent or 'ipad' in user_agent:
                    device = 'Tablet'
                else:
                    device = 'Desktop'
                
                result.update({
                    'browser': browser,
                    'os': os,
                    'device': device
                })
                
                return result
        
        # Fallback if no device info available
        return {
            'device': 'Unknown',
            'os': 'Unknown',
            'browser': 'Unknown'
        }
    
    def _extract_location_info(self, session):
        """
        extract location info from session data
        in future could use general location (country only) for security
        """
        # placeholder for now - no IP address for security
        return {
            'country': 'Unknown',
            'city': 'Unknown'
        } 