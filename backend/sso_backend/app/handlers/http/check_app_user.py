import json
import os
import sys

# Add the parent directory to sys.path to allow importing from app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from services.aws.dynamodb_service import DynamoDBService
from services.repositories.application_repository import ApplicationRepository
from services.repositories.user_repository import UserRepository
from services.auth.jwt_service import JWTService
from domains.application_domain import ApplicationDomain
from utils.response_formatter import success_response, error_response

# Initialize services and repositories
dynamodb_service = DynamoDBService()
application_repository = ApplicationRepository(dynamodb_service)
user_repository = UserRepository(dynamodb_service)
jwt_service = JWTService()
application_domain = ApplicationDomain(application_repository)

def handler(event, context):
    """
    HTTP Handler for GET /check-app-user
    Checks if user is authorized for the specified application
    
    Args:
        event: API Gateway event containing headers and query parameters
        context: Lambda context
        
    Returns:
        API Gateway response with authorization result
    """
    try:
        print("Check app user request received:", json.dumps(event))
        
        # Extract Authorization header
        headers = event.get('headers') or {}
        auth_header = headers.get('Authorization') or headers.get('authorization')
        
        if not auth_header:
            return error_response(
                status_code=401,
                message="Missing Authorization header",
                error_code="MISSING_AUTH_HEADER"
            )
        
        # Extract ID token (remove 'Bearer ' prefix if present)
        id_token = auth_header.replace('Bearer ', '') if auth_header.startswith('Bearer ') else auth_header
        
        # Extract query parameters
        query_params = event.get('queryStringParameters') or {}
        application_id = query_params.get('application_id')
        
        if not application_id:
            return error_response(
                status_code=400,
                message="Missing required parameter: application_id",
                error_code="MISSING_APPLICATION_ID"
            )
        
        # Validate ID token and extract user info
        try:
            user_info = jwt_service.extract_user_info(id_token)
            cognito_sub = user_info['sub']
        except ValueError as e:
            return error_response(
                status_code=401,
                message=f"Invalid ID token: {str(e)}",
                error_code="INVALID_TOKEN"
            )
        
        # Find user by Cognito sub
        # We use scan for sub lookup, but fall back to GSI1 for email lookup if needed
        # This handles cases where a user's sub changes after password reset
        user = application_repository.find_user_by_sub(cognito_sub)
        
        # If user not found, try to create a new user using the Cognito attributes
        if not user:
            print(f"User not found with sub: {cognito_sub}. Creating new user from token.")
            
            # Extract attributes from JWT token
            cognito_attributes = {
                'sub': cognito_sub,
                'email': user_info.get('email', ''),
                'name': user_info.get('name', ''),
                'phone_number': user_info.get('phone_number', ''),
                'gender': user_info.get('gender', ''),
                'custom:accepts_marketing': user_info.get('custom:accepts_marketing', 'false')
            }
            
            # Create the user if email exists
            if cognito_attributes['email']:
                # First check if user exists by email
                existing_user = user_repository.find_user_by_email(cognito_attributes['email'])
                
                if existing_user:
                    # Update the existing user's sub
                    print(f"Found user by email: {cognito_attributes['email']}")
                    existing_user['sub'] = cognito_sub
                    user = user_repository.update_user(existing_user)
                else:
                    # Create a new user
                    user_id, user = user_repository.create_user(cognito_attributes)
                    print(f"Created new user with ID: {user_id}")
            
            # If still no user, return error
            if not user:
                return error_response(
                    status_code=404,
                    message="User not found in system and could not be created",
                    error_code="USER_NOT_FOUND"
                )
        
        user_id = user['PK']  # Extract user_id from the user record
        
        # Check if user is authorized for the application
        is_authorized = application_repository.check_app_user_authorization(application_id, user_id)
        
        # If not authorized, create the authorization
        if not is_authorized:
            print(f"User {user_id} not authorized for application {application_id}. Creating authorization.")
            application_repository.create_app_user_relationship(application_id, user_id)
            is_authorized = True
            print(f"Authorized user {user_id} for application {application_id}")
        
        return success_response(
            data={
                "authorized": True,
                "user_id": user_id,
                "application_id": application_id,
                "user_info": {
                    "sub": cognito_sub,
                    "email": user_info.get('email'),
                    "name": user_info.get('name')
                }
            },
            message="User is authorized for the application"
        )
        
    except Exception as e:
        print(f"Error in check app user handler: {str(e)}")
        return error_response(
            status_code=500,
            message="Internal server error",
            error_code="INTERNAL_ERROR"
        ) 