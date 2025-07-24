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
        self.client_id = os.environ.get('COGNITO_APP_CLIENT_ID') 
        
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
            # First, try to get user info to check token validity and extract sub
            try:
                user_info = self.get_user_info(access_token)
                user_sub = user_info.get('sub')
                print(f"Token is valid. User sub: {user_sub}")
                print(f"Token scopes may be insufficient for direct attribute updates")
            except Exception as info_err:
                print(f"Error getting user info: {str(info_err)}")
                user_sub = None
            
            # Try direct update with access token
            try:
                response = self.cognito_client.update_user_attributes(
                    AccessToken=access_token,
                    UserAttributes=user_attributes
                )
                
                print(f"Successfully updated user attributes: {list(attributes.keys())}")
                return True
                
            except ClientError as token_err:
                error_code = token_err.response['Error']['Code']
                error_message = token_err.response['Error']['Message']
                
                print(f"Direct update failed: {error_code} - {error_message}")
                
                # If we have the user_sub from the token and it's an authorization error,
                # try admin update as a fallback
                if user_sub and error_code in ['NotAuthorizedException', 'AccessDeniedException']:
                    print(f"Attempting admin update as fallback for user {user_sub}")
                    
                    try:
                        # Use admin API as fallback (requires appropriate IAM permissions)
                        admin_response = self.cognito_client.admin_update_user_attributes(
                            UserPoolId=self.user_pool_id,
                            Username=user_sub,
                            UserAttributes=user_attributes
                        )
                        
                        print(f"Successfully updated user attributes via admin API: {list(attributes.keys())}")
                        return True
                        
                    except ClientError as admin_err:
                        admin_error_code = admin_err.response['Error']['Code']
                        admin_error_message = admin_err.response['Error']['Message']
                        
                        print(f"Admin update failed: {admin_error_code} - {admin_error_message}")
                        raise ValueError(f"Failed to update attributes: {admin_error_message}")
                else:
                    # Re-raise with more specific error messages
                    if error_code == 'NotAuthorizedException':
                        raise ValueError("Invalid or expired access token")
                    elif error_code == 'InvalidParameterException':
                        raise ValueError(f"Invalid attribute format: {error_message}")
                    else:
                        raise ClientError(token_err.response, token_err.operation_name)
                        
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
                
    def refresh_tokens(self, refresh_token):
        """
        Refresh Cognito tokens using a refresh token
        
        Args:
            refresh_token (str): The refresh token from a previous authentication
            
        Returns:
            dict: New tokens including id_token, access_token, and refresh_token
            
        Raises:
            ValueError: If refresh_token is missing or invalid
            ClientError: If Cognito API call fails
        """
        if not refresh_token:
            raise ValueError("Refresh token is required")
        
        try:
            response = self.cognito_client.initiate_auth(
                ClientId=self.client_id,
                AuthFlow='REFRESH_TOKEN_AUTH',
                AuthParameters={
                    'REFRESH_TOKEN': refresh_token
                }
            )
            
            # Extract tokens from response
            auth_result = response.get('AuthenticationResult', {})
            
            # Note: refresh_token is not returned in a refresh flow unless it's changed
            # So we need to use the original refresh token if a new one isn't provided
            tokens = {
                'id_token': auth_result.get('IdToken'),
                'access_token': auth_result.get('AccessToken'),
                'token_type': auth_result.get('TokenType', 'Bearer'),
                'expires_in': auth_result.get('ExpiresIn')
            }
            
            # Only add refresh_token if a new one was provided
            if 'RefreshToken' in auth_result:
                tokens['refresh_token'] = auth_result.get('RefreshToken')
            else:
                tokens['refresh_token'] = refresh_token
                
            print("Successfully refreshed tokens")
            return tokens
            
        except ClientError as e:
            error_code = e.response['Error']['Code']
            error_message = e.response['Error']['Message']
            
            print(f"Failed to refresh tokens: {error_code} - {error_message}")
            
            if error_code == 'NotAuthorizedException':
                raise ValueError("Invalid or expired refresh token")
            else:
                raise ClientError(e.response, e.operation_name)