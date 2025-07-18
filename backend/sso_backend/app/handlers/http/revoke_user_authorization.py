import json
import os
import sys

# Add the parent directory to sys.path to allow importing from app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from services.aws.dynamodb_service import DynamoDBService
from services.repositories.application_repository import ApplicationRepository
from services.auth.jwt_service import JWTService
from utils.response_formatter import success_response, error_response

# Initialize services and repositories
dynamodb_service = DynamoDBService()
application_repository = ApplicationRepository(dynamodb_service)
jwt_service = JWTService()

def handler(event, context):
    """
    HTTP Handler for DELETE /user-authorizations/{application_id}
    Revokes user's authorization for a specific application
    
    Args:
        event: API Gateway event containing headers and path parameters
        context: Lambda context
        
    Returns:
        API Gateway response with revocation result
    """
    try:
        print("Revoke user authorization request received:", json.dumps(event))
        
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
        
        # Extract application_id from path parameters
        path_parameters = event.get('pathParameters') or {}
        application_id = path_parameters.get('application_id')
        
        if not application_id:
            return error_response(
                status_code=400,
                message="Missing required path parameter: application_id",
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
        user = application_repository.find_user_by_sub(cognito_sub)
        if not user:
            return error_response(
                status_code=404,
                message="User not found in system",
                error_code="USER_NOT_FOUND"
            )
        
        user_id = user['PK']  # Extract user_id from the user record
        
        # Check if the authorization exists
        is_authorized = application_repository.check_app_user_authorization(application_id, user_id)
        if not is_authorized:
            return error_response(
                status_code=404,
                message="Authorization not found for this application",
                error_code="AUTHORIZATION_NOT_FOUND"
            )
        
        # Revoke the authorization using the simple jambyref schema
        application_repository.revoke_app_user_authorization(application_id, user_id)
        
        print(f"Successfully revoked authorization for user {user_id} and application {application_id}")
        
        return success_response(
            data={
                "application_id": application_id,
                "user_id": user_id,
                "status": "revoked"
            },
            message="Authorization revoked successfully"
        )
        
    except Exception as e:
        print(f"Error in revoke user authorization handler: {str(e)}")
        return error_response(
            status_code=500,
            message="Internal server error",
            error_code="INTERNAL_ERROR"
        ) 