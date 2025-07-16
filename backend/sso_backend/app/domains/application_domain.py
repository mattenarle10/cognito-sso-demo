class ApplicationDomain:
    """
    Domain class for application-related business logic.
    Handles validation and authorization for applications and channels.
    """
    
    def __init__(self, application_repository):
        """
        Initialize the ApplicationDomain with repository.
        
        Args:
            application_repository: An instance of ApplicationRepository
        """
        self.application_repository = application_repository
    
    def validate_app_channel(self, application_id, channel_id):
        """
        Validate if an application and channel combination exists.
        
        Args:
            application_id (str): The application ID
            channel_id (str): The channel ID
            
        Returns:
            tuple: (bool, str) - (is_valid, return_url)
        """
        print(f"Validating app '{application_id}' with channel '{channel_id}'")
        
        # Use the existing method from ApplicationRepository
        return self.application_repository.validate_app_channel(application_id, channel_id) 