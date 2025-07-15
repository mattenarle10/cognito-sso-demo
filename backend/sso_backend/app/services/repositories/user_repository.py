import uuid
from datetime import datetime

class UserRepository:
    """
    Repository class for User entity operations.
    Handles CRUD operations for users in DynamoDB.
    """
    
    def __init__(self, dynamodb_service):
        """
        Initialize the UserRepository with a DynamoDB service.
        
        Args:
            dynamodb_service: An instance of DynamoDBService
        """
        self.dynamodb_service = dynamodb_service
    
    def create_user(self, cognito_attributes):
        """
        Create a user record in DynamoDB from Cognito attributes.
        
        Args:
            cognito_attributes (dict): User attributes from Cognito
            
        Returns:
            str: The generated user_id
            dict: The created user item
        """
        # Generate a unique user_id
        user_id = f"user-{str(uuid.uuid4())[:8]}"
        
        # Extract attributes from Cognito
        cognito_sub = cognito_attributes['sub']
        email = cognito_attributes['email']
        name = cognito_attributes.get('name', '')
        phone_number = cognito_attributes.get('phone_number', '')
        gender = cognito_attributes.get('custom:gender', '')
        accepts_marketing = cognito_attributes.get('custom:accepts_marketing', 'false')
        
        # Current timestamp
        timestamp = datetime.now().isoformat()
        
        # Create user record
        user_item = {
            "PK": user_id,
            "SK": "user",
            "sub": cognito_sub,
            "email": email,
            "name": name,
            "phone_number": phone_number,
            "gender": gender,
            "accepts_marketing": accepts_marketing,
            "created_at": timestamp
        }
        
        # Save to DynamoDB
        self.dynamodb_service.put_item(user_item)
        
        return user_id, user_item
    
    def get_user_by_id(self, user_id):
        """
        Get a user by user_id.
        
        Args:
            user_id (str): The user ID
            
        Returns:
            dict: The user item
        """
        key = {
            "PK": user_id,
            "SK": "user"
        }
        return self.dynamodb_service.get_item(key)
    
    def get_user_by_sub(self, cognito_sub):
        """
        Get a user by Cognito sub (requires a scan or GSI).
        This is a simplified implementation and would need a GSI in production.
        
        Args:
            cognito_sub (str): The Cognito sub
            
        Returns:
            dict: The user item
        """
        # In a real implementation, you would use a GSI on the sub attribute
        # For now, we'll just return None as this requires a full table scan
        return None
