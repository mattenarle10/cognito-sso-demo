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
        Register a new user and authorize them for an application.
        
        Args:
            cognito_attributes (dict): User attributes from Cognito
            application_id (str): The application ID to authorize the user for
            
        Returns:
            str: The generated user_id
            dict: The created user item
        """
        # Create the user in DynamoDB
        user_id, user_item = self.user_repository.create_user(cognito_attributes)
        
        # Create the application-user relationship
        self.application_repository.create_app_user_relationship(application_id, user_id)
        
        return user_id, user_item
