import uuid
from datetime import datetime, timedelta

class SessionRepository:
    """
    repository for session operations - storing and retrieving session data
    sessions store cognito tokens so client apps can get them later
    """
    
    def __init__(self, dynamodb_service):
        """initialize with dynamodb service"""
        self.dynamodb_service = dynamodb_service
    
    def create_session(self, user_id, cognito_tokens, application_id):
        """
        create a new session and store cognito tokens
        
        args:
            user_id (str): the user id
            cognito_tokens (dict): tokens from cognito (id_token, access_token, etc)
            application_id (str): which app this session is for
            
        returns:
            str: the generated session_id
        """
        # generate unique session id
        session_id = f"session-{str(uuid.uuid4())[:8]}"
        
        # calculate expiration (24 hours from now)
        expires_at = (datetime.now() + timedelta(hours=24)).isoformat()
        timestamp = datetime.now().isoformat()
        
        # create session record
        session_item = {
            "PK": session_id,
            "SK": "session",
            "user_id": user_id,
            "application_id": application_id,
            "id_token": cognito_tokens.get('id_token'),
            "access_token": cognito_tokens.get('access_token'), 
            "refresh_token": cognito_tokens.get('refresh_token'),
            "token_type": cognito_tokens.get('token_type', 'Bearer'),
            "expires_in": cognito_tokens.get('expires_in'),
            "expires_at": expires_at,
            "created_at": timestamp
        }
        
        # save to dynamodb
        self.dynamodb_service.put_item(session_item)
        
        return session_id
    
    def get_session(self, session_id):
        """
        get session data by session_id
        
        args:
            session_id (str): the session id
            
        returns:
            dict: session data with tokens, or none if not found/expired
        """
        key = {
            "PK": session_id,
            "SK": "session"
        }
        
        session = self.dynamodb_service.get_item(key)
        
        if not session:
            return None
            
        # check if session is expired
        expires_at = session.get('expires_at')
        if expires_at:
            expiry_time = datetime.fromisoformat(expires_at)
            if datetime.now() > expiry_time:
                print(f"session {session_id} is expired")
                return None
        
        return session
    
    def delete_session(self, session_id):
        """
        delete a session (for logout)
        
        args:
            session_id (str): the session id
        """
        key = {
            "PK": session_id,
            "SK": "session"
        }
        
        self.dynamodb_service.main_table.delete_item(Key=key)
    
    def get_user_sessions(self, user_id, include_expired=False):
        """
        get all sessions for a specific user
        
        args:
            user_id (str): the user id
            include_expired (bool): whether to include expired sessions
            
        returns:
            dict: {'active': [...], 'expired': [...]}
        """
        import boto3
        from boto3.dynamodb.conditions import Attr
        
        try:
            # scan for session records with matching user_id
            response = self.dynamodb_service.dynamodb.Table(self.dynamodb_service.main_table_name).scan(
                FilterExpression=Attr('SK').eq('session') & Attr('user_id').eq(user_id)
            )
            
            sessions = response.get('Items', [])
            active_sessions = []
            expired_sessions = []
            
            current_time = datetime.now()
            
            for session in sessions:
                # check if session is expired
                expires_at = session.get('expires_at')
                is_expired = False
                
                if expires_at:
                    try:
                        expiry_time = datetime.fromisoformat(expires_at)
                        is_expired = current_time > expiry_time
                    except ValueError:
                        # invalid date format, consider expired
                        is_expired = True
                
                # categorize session
                if is_expired:
                    if include_expired:
                        expired_sessions.append(session)
                else:
                    active_sessions.append(session)
            
            return {
                'active': active_sessions,
                'expired': expired_sessions
            }
            
        except Exception as e:
            print(f"error getting user sessions: {str(e)}")
            return {'active': [], 'expired': []}
    
    def revoke_all_user_sessions(self, user_id, except_session_id=None):
        """
        revoke all sessions for a user (useful for security)
        
        args:
            user_id (str): the user id
            except_session_id (str): session to keep active (current session)
            
        returns:
            int: number of sessions revoked
        """
        sessions_data = self.get_user_sessions(user_id, include_expired=False)
        active_sessions = sessions_data['active']
        
        revoked_count = 0
        
        for session in active_sessions:
            session_id = session['PK']
            
            # skip the current session if specified
            if except_session_id and session_id == except_session_id:
                continue
            
            try:
                self.delete_session(session_id)
                revoked_count += 1
                print(f"revoked session: {session_id}")
            except Exception as e:
                print(f"failed to revoke session {session_id}: {str(e)}")
        
        return revoked_count 