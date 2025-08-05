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
    
    def find_user_by_sub(self, cognito_sub):
        """
        Find a user by their Cognito sub.
        First tries direct lookup by sub, then falls back to email lookup if available.
        
        Args:
            cognito_sub (str): The Cognito sub
            
        Returns:
            dict: The user item if found, None otherwise
        """
        from services.repositories.user_repository import UserRepository
        
        try:
            # First attempt: direct lookup by sub (still using scan as there's no GSI for sub)
            import boto3
            from boto3.dynamodb.conditions import Key, Attr
            
            # Scan for user records with matching sub
            response = self.dynamodb_service.dynamodb.Table(self.dynamodb_service.main_table_name).scan(
                FilterExpression=Attr('SK').eq("user") & Attr('sub').eq(cognito_sub),
                Limit=1  # We only need one match
            )
            
            items = response.get('Items', [])
            if items:
                print(f"Found user directly by sub: {cognito_sub}")
                return items[0]
            
            # Second attempt: If user not found by sub, try to get their email from Cognito
            # and use the GSI to find them by email
            try:
                from services.aws.cognito_user_service import CognitoUserService
                cognito_service = CognitoUserService()
                
                # Get user attributes from Cognito using the sub
                user_attributes = cognito_service.get_user_by_sub(cognito_sub)
                if user_attributes and 'email' in user_attributes:
                    email = user_attributes['email']
                    print(f"Looking for user by email: {email} using GSI")
                    
                    # Use UserRepository to find by email using GSI1
                    user_repo = UserRepository(self.dynamodb_service)
                    user_item = user_repo.find_user_by_email(email)
                    
                    if user_item:
                        print(f"Found user by email GSI: {email}")
                        # Update the user's sub to match the new one
                        user_item['sub'] = cognito_sub
                        
                        # Save the updated user item
                        self.dynamodb_service.put_item(user_item)
                        return user_item
                    else:
                        print(f"No user found with email: {email}")
            except Exception as email_error:
                print(f"Error finding user by email: {str(email_error)}")
            
            return None
            
        except Exception as e:
            print(f"Error finding user by sub: {str(e)}")
            return None
    
    def get_user_authorization(self, application_id, user_id):
        """
        Get user authorization for an application.
        
        Args:
            application_id (str): The application ID
            user_id (str): The user ID
            
        Returns:
            dict: The authorization item if found, None otherwise
        """
        key = {
            "PK": f"authorization-{application_id}",
            "SK": user_id
        }
        return self.dynamodb_service.get_item(key)
    
    def create_user_authorization(self, application_id, user_id, scopes_granted):
        """
        Create or update user authorization for an application with specific scopes.
        
        Args:
            application_id (str): The application ID
            user_id (str): The user ID
            scopes_granted (list): List of scopes the user granted
            
        Returns:
            dict: The created authorization item
        """
        from datetime import datetime
        
        # Current timestamp
        timestamp = datetime.now().isoformat()
        
        # Create authorization record with granular scopes
        authorization_item = {
            "PK": f"authorization-{application_id}",
            "SK": user_id,
            "application_id": application_id,
            "user_id": user_id,
            "scopes_granted": scopes_granted,
            "status": "active",
            "granted_at": timestamp
        }
        
        # Save to DynamoDB
        self.dynamodb_service.put_item(authorization_item)
        
        return authorization_item
    
    def revoke_user_authorization(self, application_id, user_id):
        """
        Revoke user authorization for an application.
        
        Args:
            application_id (str): The application ID
            user_id (str): The user ID
        """
        from datetime import datetime
        
        # Get existing authorization
        authorization = self.get_user_authorization(application_id, user_id)
        if authorization:
            # Update status to revoked
            authorization['status'] = 'revoked'
            authorization['revoked_at'] = datetime.now().isoformat()
            
            # Save updated item
            self.dynamodb_service.put_item(authorization)
    
    def check_user_scope_authorization(self, application_id, user_id, required_scopes):
        """
        Check if user has authorized specific scopes for an application.
        
        Args:
            application_id (str): The application ID
            user_id (str): The user ID
            required_scopes (list): List of scopes required
            
        Returns:
            tuple: (bool, list) - (has_all_scopes, missing_scopes)
        """
        authorization = self.get_user_authorization(application_id, user_id)
        
        if not authorization or authorization.get('status') != 'active':
            return False, required_scopes
        
        granted_scopes = authorization.get('scopes_granted', [])
        missing_scopes = [scope for scope in required_scopes if scope not in granted_scopes]
        
        return len(missing_scopes) == 0, missing_scopes
    
    def get_user_authorizations(self, user_id):
        """
        Get all applications that a user has authorized.
        Uses the simple jambyref schema where PK = application-{app_id} and SK = user_id
        
        Args:
            user_id (str): The user ID
            
        Returns:
            list: List of authorized applications with details
        """
        import boto3
        from boto3.dynamodb.conditions import Key, Attr
        
        try:
            # Query for all items where SK = user_id and PK starts with "application-"
            response = self.dynamodb_service.dynamodb.Table(self.dynamodb_service.main_table_name).scan(
                FilterExpression=Attr('SK').eq(user_id) & Attr('PK').begins_with('application-')
            )
            
            authorizations = []
            for item in response.get('Items', []):
                # Extract application_id from PK
                app_id = item['PK'].replace('application-', '')
                
                # Get application details
                application = self.get_application(app_id)
                
                authorization_info = {
                    "application_id": app_id,
                    "application_name": application.get('name', app_id) if application else app_id,
                    "application_description": application.get('description', '') if application else '',
                    "created_at": item.get('created_at'),
                    "status": "active"  # Simple schema assumes active if record exists
                }
                
                authorizations.append(authorization_info)
            
            return authorizations
            
        except Exception as e:
            print(f"Error getting user authorizations: {str(e)}")
            return []
    
    def revoke_app_user_authorization(self, application_id, user_id):
        """
        Revoke user authorization for an application using the simple jambyref schema.
        Simply deletes the application-user relationship record.
        
        Args:
            application_id (str): The application ID
            user_id (str): The user ID
        """
        try:
            key = {
                "PK": f"application-{application_id}",
                "SK": user_id
            }
            
            # Delete the authorization record
            self.dynamodb_service.dynamodb.Table(self.dynamodb_service.main_table_name).delete_item(Key=key)
            print(f"Revoked authorization for user {user_id} and application {application_id}")
            
        except Exception as e:
            print(f"Error revoking authorization: {str(e)}")
            raise