from datetime import datetime

class ApplicationRepository:
    """
    Repository class for Application entity operations.
    Handles CRUD operations for applications and application-user relationships in DynamoDB.
    """
    
    def __init__(self, dynamodb_service):
        """
        Initialize the ApplicationRepository with a DynamoDB service.
        
        Args:
            dynamodb_service: An instance of DynamoDBService
        """
        self.dynamodb_service = dynamodb_service
    
    def get_application(self, application_id):
        """
        Get an application by ID.
        
        Args:
            application_id (str): The application ID
            
        Returns:
            dict: The application item
        """
        key = {
            "PK": f"application-{application_id}",
            "SK": "application"
        }
        return self.dynamodb_service.get_item(key)
    
    def create_app_user_relationship(self, application_id, user_id):
        """
        Create an application-user relationship record in DynamoDB.
        This authorizes a user for an application.
        
        Args:
            application_id (str): The application ID
            user_id (str): The user ID
            
        Returns:
            dict: The created application-user item
        """
        # Current timestamp
        timestamp = datetime.now().isoformat()
        
        # Create application-user relationship record
        app_user_item = {
            "PK": f"application-{application_id}",
            "SK": user_id,
            "application_id": application_id,
            "user_id": user_id,
            "created_at": timestamp
        }
        
        # Save to DynamoDB
        self.dynamodb_service.put_item(app_user_item)
        
        return app_user_item
    
    def check_app_user_authorization(self, application_id, user_id):
        """
        Check if a user is authorized for an application.
        
        Args:
            application_id (str): The application ID
            user_id (str): The user ID
            
        Returns:
            bool: True if authorized, False otherwise
        """
        key = {
            "PK": f"application-{application_id}",
            "SK": user_id
        }
        item = self.dynamodb_service.get_item(key)
        return item is not None
    
    def validate_app_channel(self, application_id, channel_id):
        """
        Validate if an application and channel combination exists.
        
        Args:
            application_id (str): The application ID
            channel_id (str): The channel ID
            
        Returns:
            tuple: (bool, str) - (is_valid, return_url)
        """
        # Get the application
        application = self.get_application(application_id)
        
        if not application:
            return False, None
        
        # Check if the channel exists
        channels = application.get('channels', [])
        for channel in channels:
            if channel.get('channel_id') == channel_id:
                return True, channel.get('return_url')
        
        return False, None
