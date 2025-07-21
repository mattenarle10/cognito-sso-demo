import uuid
from datetime import datetime
import boto3
from boto3.dynamodb.conditions import Key

class UserRepository:
    """
    Repository class for User entity operations.
    Handles CRUD operations for users in DynamoDB.
    Uses GSIs for efficient lookups by email, phone, and session ID.
    """
    
    def __init__(self, dynamodb_service):
        """
        Initialize the UserRepository with a DynamoDB service.
        
        Args:
            dynamodb_service: An instance of DynamoDBService
        """
        self.dynamodb_service = dynamodb_service
        self.table_name = dynamodb_service.table_name
    
    def create_user(self, cognito_attributes):
        """
        Create a user record in DynamoDB from Cognito attributes.
        Also creates GSI entries for email and phone lookups.
        
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
        gender = cognito_attributes.get('gender', '')
        accepts_marketing = cognito_attributes.get('custom:accepts_marketing', 'false')
        
        # Current timestamp
        timestamp = datetime.now().isoformat()
        
        # Create user record with GSI attributes
        user_item = {
            "PK": user_id,
            "SK": "user",
            "sub": cognito_sub,
            "email": email,
            "name": name,
            "phone_number": phone_number,
            "gender": gender,
            "accepts_marketing": accepts_marketing,
            "created_at": timestamp,
            "user_name": user_id,  # Store user_id as user_name for consistency
            # GSI1 for email lookups
            "GSI1-PK": f"email-{email}",
            "GSI1-SK": "user",
        }
        
        # Add phone number GSI if phone is provided
        if phone_number:
            user_item["GSI2-PK"] = f"phone-{phone_number}"
            user_item["GSI2-SK"] = "user"
        
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
        Get a user by Cognito sub.
        
        Args:
            cognito_sub (str): The Cognito sub
            
        Returns:
            dict: The user item
        """
        # For sub lookups, we still need to scan since we don't have a GSI for it
        # In a production environment, we would add a GSI for sub lookups
        items = self.dynamodb_service.scan({
            'FilterExpression': 'sub = :sub',
            'ExpressionAttributeValues': {':sub': cognito_sub}
        })
        
        # Return the first matching item or None
        return items[0] if items else None
        
    def find_user_by_email(self, email):
        """
        Find a user by email address using GSI1.
        
        Args:
            email (str): The email address
            
        Returns:
            dict: The user item or None if not found
        """
        # Use GSI1 to query by email
        key_condition = Key('GSI1-PK').eq(f"email-{email}") & Key('GSI1-SK').eq("user")
        
        # Query the GSI
        response = self.dynamodb_service.query_index({
            'IndexName': 'GSI1',
            'KeyConditionExpression': key_condition
        })
        
        # Return the first matching item or None
        items = response.get('Items', [])
        return items[0] if items else None
    
    def find_user_by_phone(self, phone_number):
        """
        Find a user by phone number using GSI2.
        
        Args:
            phone_number (str): The phone number
            
        Returns:
            dict: The user item or None if not found
        """
        # Use GSI2 to query by phone number
        key_condition = Key('GSI2-PK').eq(f"phone-{phone_number}") & Key('GSI2-SK').eq("user")
        
        # Query the GSI
        response = self.dynamodb_service.query_index({
            'IndexName': 'GSI2',
            'KeyConditionExpression': key_condition
        })
        
        # Return the first matching item or None
        items = response.get('Items', [])
        return items[0] if items else None
    
    def update_user(self, user_item):
        """
        Update an existing user record.
        
        Args:
            user_item (dict): The user item to update
            
        Returns:
            dict: The updated user item
        """
        # Update the item in DynamoDB
        self.dynamodb_service.put_item(user_item)
        return user_item
        
    def link_social_provider(self, user_item, provider_name, provider_user_id):
        """
        Link a social provider to an existing user.
        
        Args:
            user_item (dict): The existing user item
            provider_name (str): The name of the social provider (e.g., 'Google', 'Facebook')
            provider_user_id (str): The user ID from the social provider
            
        Returns:
            dict: The updated user item
        """
        # Initialize social_providers if it doesn't exist
        if 'social_providers' not in user_item:
            user_item['social_providers'] = {}
            
        # Add or update the provider entry
        user_item['social_providers'][provider_name] = {
            'id': provider_user_id,
            'linked_at': datetime.now().isoformat()
        }
        
        # Update the item in DynamoDB
        self.dynamodb_service.put_item(user_item)
        return user_item
