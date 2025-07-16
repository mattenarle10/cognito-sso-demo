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