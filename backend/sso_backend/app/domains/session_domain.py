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
        if not user:
            raise ValueError("user not found in system")
        
        user_id = user['PK']  # extract user_id
        
        # Check if user is authorized for this application (jambyref.md simple schema)
        is_authorized = self.application_repository.check_app_user_authorization(application_id, user_id)
        if not is_authorized:
            raise ValueError(f"user not authorized for application {application_id}")
        
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
        return self.session_repository.get_session(session_id)
    
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