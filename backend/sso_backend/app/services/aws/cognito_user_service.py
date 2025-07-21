import os
import boto3
from botocore.exceptions import ClientError

class CognitoUserService:
    """
    Service for managing Cognito user attributes and profile information
    """
    
    def __init__(self):
        """Initialize Cognito client with environment configuration"""
        self.cognito_client = boto3.client('cognito-idp', region_name=os.environ.get('AWS_REGION', 'ap-southeast-2'))
        self.user_pool_id = os.environ.get('COGNITO_USER_POOL_ID')
        
        if not self.user_pool_id:
            raise ValueError("COGNITO_USER_POOL_ID environment variable is required")
    
    def update_user_attributes(self, access_token, attributes):
        """
        Update user attributes in Cognito
        
        Args:
            access_token (str): User's Cognito access token
            attributes (dict): Dictionary of attributes to update (e.g., {'name': 'New Name'})
            
        Returns:
            bool: True if successful, False otherwise
            
        Raises:
            ValueError: If access_token is missing or attributes are invalid
            ClientError: If Cognito API call fails
        """
        if not access_token:
            raise ValueError("Access token is required")
        
        if not attributes or not isinstance(attributes, dict):
            raise ValueError("Attributes must be a non-empty dictionary")
        
        # Convert attributes to Cognito format
        user_attributes = []
        for key, value in attributes.items():
            user_attributes.append({
                'Name': key,
                'Value': str(value)
            })
        
        try:
            response = self.cognito_client.update_user_attributes(
                AccessToken=access_token,
                UserAttributes=user_attributes
            )
            
            print(f"Successfully updated user attributes: {list(attributes.keys())}")
            return True
            
        except ClientError as e:
            error_code = e.response['Error']['Code']
            error_message = e.response['Error']['Message']
            
            print(f"Failed to update user attributes: {error_code} - {error_message}")
            
            # Re-raise with more specific error messages
            if error_code == 'NotAuthorizedException':
                raise ValueError("Invalid or expired access token")
            elif error_code == 'InvalidParameterException':
                raise ValueError(f"Invalid attribute format: {error_message}")
            else:
                raise ClientError(e.response, e.operation_name)
    
    def get_user_info(self, access_token):
        """
        Get user information from Cognito using access token
        
        Args:
            access_token (str): User's Cognito access token
            
        Returns:
            dict: User information from Cognito
            
        Raises:
            ValueError: If access_token is missing
            ClientError: If Cognito API call fails
        """
        if not access_token:
            raise ValueError("Access token is required")
        
        try:
            response = self.cognito_client.get_user(AccessToken=access_token)
            
            # Convert UserAttributes to a more usable format
            user_info = {
                'username': response.get('Username'),
                'user_status': response.get('UserStatus'),
                'enabled': response.get('Enabled', True)
            }
            
            # Parse attributes
            for attr in response.get('UserAttributes', []):
                user_info[attr['Name']] = attr['Value']
            
            return user_info
            
        except ClientError as e:
            error_code = e.response['Error']['Code']
            error_message = e.response['Error']['Message']
            
            print(f"Failed to get user info: {error_code} - {error_message}")
            
            if error_code == 'NotAuthorizedException':
                raise ValueError("Invalid or expired access token")
            else:
                raise ClientError(e.response, e.operation_name) 