import os
import boto3
import json
from datetime import datetime


class CognitoAdminService:
    """
    Service for Cognito User Pool admin operations
    Handles all admin-level operations on Cognito users
    """

    def __init__(self):
        """Initialize Cognito service with user pool information from environment"""
        self.cognito = boto3.client('cognito-idp')
        self.user_pool_id = os.environ.get('COGNITO_USER_POOL_ID')
        self.app_client_id = os.environ.get('COGNITO_APP_CLIENT_ID')

    def _format_user_attributes(self, attributes):
        """
        Format Cognito user attributes into a dictionary
        
        Args:
            attributes (list): List of Cognito attribute objects
            
        Returns:
            dict: Dictionary of attribute name-value pairs
        """
        if not attributes:
            return {}
        
        return {attr['Name']: attr['Value'] for attr in attributes}
    
    def _convert_cognito_datetime(self, dt_str):
        """
        Convert Cognito datetime to ISO format string
        
        Args:
            dt_str: Datetime object or string from Cognito
            
        Returns:
            str: ISO formatted datetime string
        """
        if not dt_str:
            return None
            
        if isinstance(dt_str, datetime):
            return dt_str.isoformat()
        return dt_str

    def list_users(self, limit=25, pagination_token=None, filter_expr=None):
        """
        List users in the Cognito User Pool with optional filtering
        
        Args:
            limit (int): Maximum number of users to return
            pagination_token (str): Token for pagination
            filter_expr (str): Filter expression for Cognito ListUsers API
            
        Returns:
            dict: Response containing users and pagination token
        """
        try:
            params = {
                'UserPoolId': self.user_pool_id,
                'Limit': limit
            }
            
            if pagination_token:
                params['PaginationToken'] = pagination_token
                
            if filter_expr:
                params['Filter'] = filter_expr
                
            response = self.cognito.list_users(**params)
            
            # Format the user data
            formatted_users = []
            for user in response.get('Users', []):
                formatted_user = {
                    'username': user.get('Username'),
                    'user_status': user.get('UserStatus'),
                    'enabled': user.get('Enabled', True),
                    'user_create_date': self._convert_cognito_datetime(user.get('UserCreateDate')),
                    'user_last_modified_date': self._convert_cognito_datetime(user.get('UserLastModifiedDate')),
                    'attributes': self._format_user_attributes(user.get('Attributes', []))
                }
                formatted_users.append(formatted_user)
                
            result = {
                'users': formatted_users,
                'pagination_token': response.get('PaginationToken')
            }
            
            return result
            
        except Exception as e:
            print(f"Error listing users: {str(e)}")
            raise
    
    def get_user(self, username):
        """
        Get detailed information for a specific user
        
        Args:
            username (str): Cognito username
            
        Returns:
            dict: User information
        """
        try:
            response = self.cognito.admin_get_user(
                UserPoolId=self.user_pool_id,
                Username=username
            )
            
            # Format the user data
            user_data = {
                'username': response.get('Username'),
                'user_status': response.get('UserStatus'),
                'enabled': response.get('Enabled', True),
                'user_create_date': self._convert_cognito_datetime(response.get('UserCreateDate')),
                'user_last_modified_date': self._convert_cognito_datetime(response.get('UserLastModifiedDate')),
                'attributes': self._format_user_attributes(response.get('UserAttributes', []))
            }
            
            return user_data
            
        except self.cognito.exceptions.UserNotFoundException:
            print(f"User not found: {username}")
            return None
        except Exception as e:
            print(f"Error getting user {username}: {str(e)}")
            raise
    
    def update_user_attributes(self, username, attributes):
        """
        Update attributes for a user
        
        Args:
            username (str): Cognito username
            attributes (dict): Dictionary of attribute name-value pairs
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            user_attributes = [
                {'Name': key, 'Value': str(value)} 
                for key, value in attributes.items()
            ]
            
            self.cognito.admin_update_user_attributes(
                UserPoolId=self.user_pool_id,
                Username=username,
                UserAttributes=user_attributes
            )
            
            return True
            
        except Exception as e:
            print(f"Error updating attributes for user {username}: {str(e)}")
            return False
    
    def force_password_reset(self, username):
        """
        Force a user to reset their password on next login
        
        Args:
            username (str): Cognito username
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            self.cognito.admin_reset_user_password(
                UserPoolId=self.user_pool_id,
                Username=username
            )
            
            return True
            
        except Exception as e:
            print(f"Error forcing password reset for user {username}: {str(e)}")
            return False
    
    def deactivate_user(self, username):
        """
        Disable a user account
        
        Args:
            username (str): Cognito username
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            self.cognito.admin_disable_user(
                UserPoolId=self.user_pool_id,
                Username=username
            )
            
            return True
            
        except Exception as e:
            print(f"Error deactivating user {username}: {str(e)}")
            return False
    
    def activate_user(self, username):
        """
        Enable a disabled user account
        
        Args:
            username (str): Cognito username
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            self.cognito.admin_enable_user(
                UserPoolId=self.user_pool_id,
                Username=username
            )
            
            return True
            
        except Exception as e:
            print(f"Error activating user {username}: {str(e)}")
            return False
    
    def delete_user(self, username):
        """
        Delete a user from the Cognito User Pool
        
        Args:
            username (str): Cognito username
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            self.cognito.admin_delete_user(
                UserPoolId=self.user_pool_id,
                Username=username
            )
            
            return True
            
        except Exception as e:
            print(f"Error deleting user {username}: {str(e)}")
            return False
