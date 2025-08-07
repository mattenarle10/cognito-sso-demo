import json
import sys
import os

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from utils.response_formatter import success_response, error_response
from services.auth.jwt_service import JWTService
from services.aws.cognito_user_service import CognitoUserService
from services.aws.dynamodb_service import DynamoDBService
from services.repositories.user_repository import UserRepository
from services.repositories.application_repository import ApplicationRepository
from domains.user_profile_domain import UserProfileDomain

# Initialize services and domain
jwt_service = JWTService()
cognito_user_service = CognitoUserService()
dynamodb_service = DynamoDBService()
user_repository = UserRepository(dynamodb_service)
application_repository = ApplicationRepository(dynamodb_service)
user_profile_domain = UserProfileDomain(cognito_user_service, user_repository)

def handler(event, context):
    """
    HTTP Handler for PATCH /user-profile
    Updates user profile information in Cognito
    
    Args:
        event: API Gateway event containing PATCH body and Authorization header
        context: Lambda context
        
    Returns:
        API Gateway response with updated profile status
    """
    try:
        print("Update user profile request received:", json.dumps(event))
        
        # Extract and validate Authorization header
        headers = event.get('headers', {})
        auth_header = headers.get('authorization') or headers.get('Authorization')
        
        if not auth_header or not auth_header.startswith('Bearer '):
            return error_response(
                status_code=401,
                message="Missing or invalid Authorization header",
                error_code="MISSING_AUTH_HEADER"
            )
        
        # Extract tokens
        id_token = auth_header.replace('Bearer ', '')
        
        # Validate the ID token and extract user info
        try:
            user_info = jwt_service.extract_user_info(id_token)
            cognito_sub = user_info['sub']
        except ValueError as e:
            return error_response(
                status_code=401,
                message=f"Invalid token: {str(e)}",
                error_code="INVALID_TOKEN"
            )
        
        # Find user in DynamoDB (CRITICAL for authorization system)
        user = application_repository.find_user_by_sub(cognito_sub)
        
        # Debug: Print user lookup details
        print(f"Looking for user with sub: {cognito_sub}")
        
        # If not found by sub directly, try to find by email (for OAuth users)
        if not user and 'email' in user_info:
            print(f"User not found by sub, trying email lookup: {user_info['email']}")
            user = user_repository.find_user_by_email(user_info['email'])
            
            if user:
                print(f"Found user by email: {user_info['email']}")
                # Update the user's sub to match the current one
                user['sub'] = cognito_sub
                user_repository.update_user(user)
        
        if not user:
            print(f"User not found in DynamoDB with sub: {cognito_sub} or email: {user_info.get('email', 'N/A')}")
            return error_response(
                status_code=404,
                message="User not found in system",
                error_code="USER_NOT_FOUND"
            )
        
        user_id = user['PK']  # Extract user_id from DynamoDB
        print(f"Found user with ID: {user_id}")
        
        # Extract request body
        body = event.get('body')
        if not body:
            return error_response(
                status_code=400,
                message="Missing request body",
                error_code="MISSING_BODY"
            )
        
        # Parse JSON body
        try:
            request_data = json.loads(body)
        except json.JSONDecodeError:
            return error_response(
                status_code=400,
                message="Invalid JSON in request body",
                error_code="INVALID_JSON"
            )
        
        # Validate required fields
        updates = request_data.get('updates', {})
        access_token = request_data.get('access_token')
        
        if not updates:
            return error_response(
                status_code=400,
                message="No updates provided",
                error_code="NO_UPDATES"
            )
        
        if not access_token:
            return error_response(
                status_code=400,
                message="Access token is required for profile updates",
                error_code="MISSING_ACCESS_TOKEN"
            )
        
        # Use domain layer for proper validation and sync
        try:
            result = user_profile_domain.update_user_profile(access_token, user_id, updates)
            
            return success_response(
                data=result,
                message="Profile updated successfully"
            )
            
        except ValueError as e:
            return error_response(
                status_code=400,
                message=str(e),
                error_code="VALIDATION_ERROR"
            )
        except Exception as e:
            print(f"Unexpected error updating profile: {str(e)}")
            return error_response(
                status_code=500,
                message="Internal server error",
                error_code="INTERNAL_ERROR"
            )
    
    except Exception as e:
        print(f"Unexpected error in update_user_profile handler: {str(e)}")
        return error_response(
            status_code=500,
            message="Internal server error",
            error_code="INTERNAL_ERROR"
        ) 