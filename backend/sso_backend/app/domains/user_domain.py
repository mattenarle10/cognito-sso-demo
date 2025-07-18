class UserDomain:
    """
    Domain class for user-related business logic.
    Coordinates between repositories for user operations.
    """
    
    def __init__(self, user_repository, application_repository):
        """
        Initialize the UserDomain with repositories.
        
        Args:
            user_repository: An instance of UserRepository
            application_repository: An instance of ApplicationRepository
        """
        self.user_repository = user_repository
        self.application_repository = application_repository
    
    def register_user(self, cognito_attributes, application_id):
        """
        Register a new user WITHOUT automatically authorizing them for an application.
        User will need to provide consent on first login.
        
        Args:
            cognito_attributes (dict): User attributes from Cognito
            application_id (str): The application ID (for logging purposes)
            
        Returns:
            str: The generated user_id
            dict: The created user item
        """
        # Create the user in DynamoDB
        user_id, user_item = self.user_repository.create_user(cognito_attributes)
        
        # DO NOT auto-authorize - user must consent on first login
        # self.application_repository.create_app_user_relationship(application_id, user_id)
        
        print(f"Successfully created user {user_id} - will require consent for application {application_id}")
        
        return user_id, user_item
