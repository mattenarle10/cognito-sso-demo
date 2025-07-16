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
    
    def initialize_session(self, cognito_tokens, application_id):
        """
        initialize a new session with cognito tokens
        validates user authorization for the application first
        
        args:
            cognito_tokens (dict): tokens from cognito
            application_id (str): the application requesting session
            
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
        
        # check if user is authorized for this application
        is_authorized = self.application_repository.check_app_user_authorization(application_id, user_id)
        if not is_authorized:
            raise ValueError(f"user not authorized for application {application_id}")
        
        # create the session with tokens
        session_id = self.session_repository.create_session(user_id, cognito_tokens, application_id)
        
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