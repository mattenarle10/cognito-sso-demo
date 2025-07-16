import json
import os
import sys

# Add the parent directory to sys.path to allow importing from app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from services.aws.dynamodb_service import DynamoDBService
from services.repositories.application_repository import ApplicationRepository
from services.auth.jwt_service import JWTService
from domains.application_domain import ApplicationDomain
from utils.response_formatter import success_response, error_response

# Initialize services and repositories
dynamodb_service = DynamoDBService()
application_repository = ApplicationRepository(dynamodb_service)
jwt_service = JWTService()
application_domain = ApplicationDomain(application_repository)

def handler(event, context):
    """
    HTTP Handler for POST /authorize-application
    Handles user consent and creates authorization grants for applications
    
    Args:
        event: API Gateway event containing POST body with authorization data
        context: Lambda context
        
    Returns:
        API Gateway response with authorization result
    """
    try:
        print("Authorize application request received:", json.dumps(event))
        
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
        
        # Extract required fields
        application_id = request_data.get('application_id')
        granted_scopes = request_data.get('granted_scopes', [])
        action = request_data.get('action')  # 'approve' or 'deny'
        
        if not application_id:
            return error_response(
                status_code=400,
                message="Missing required field: application_id",
                error_code="MISSING_APPLICATION_ID"
            )
        
        if not action or action not in ['approve', 'deny']:
            return error_response(
                status_code=400,
                message="Invalid action. Must be 'approve' or 'deny'",
                error_code="INVALID_ACTION"
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
        
        # Validate that the application exists
        application = application_repository.get_application(application_id)
        if not application:
            return error_response(
                status_code=404,
                message="Application not found",
                error_code="APPLICATION_NOT_FOUND"
            )
        
        if action == 'deny':
            # User denied authorization - we can log this but don't create any grants
            print(f"User {user_id} denied authorization for application {application_id}")
            return success_response(
                data={
                    "status": "denied",
                    "message": "Authorization denied by user"
                }
            )
        
        # User approved - validate and create authorization
        if not granted_scopes:
            return error_response(
                status_code=400,
                message="No scopes granted",
                error_code="NO_SCOPES_GRANTED"
            )
        
        # Create authorization grant
        authorization = application_repository.create_user_authorization(
            application_id, 
            user_id, 
            granted_scopes
        )
        
        print(f"Created authorization for user {user_id} and application {application_id} with scopes: {granted_scopes}")
        
        return success_response(
            data={
                "status": "approved",
                "authorization_id": f"{application_id}-{user_id}",
                "scopes_granted": granted_scopes,
                "granted_at": authorization['granted_at'],
                "message": "Authorization granted successfully"
            }
        )
        
    except Exception as e:
        print(f"Error in authorize application handler: {str(e)}")
        return error_response(
            status_code=500,
            message="Internal server error",
            error_code="INTERNAL_ERROR"
        ) 