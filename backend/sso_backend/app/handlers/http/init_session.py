import json
import os
import sys

# Add the parent directory to sys.path to allow importing from app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from services.aws.dynamodb_service import DynamoDBService
from services.repositories.application_repository import ApplicationRepository
from services.repositories.session_repository import SessionRepository
from services.auth.jwt_service import JWTService
from domains.session_domain import SessionDomain
from utils.response_formatter import success_response, error_response

# Initialize services and repositories
dynamodb_service = DynamoDBService()
application_repository = ApplicationRepository(dynamodb_service)
session_repository = SessionRepository(dynamodb_service)
jwt_service = JWTService()
session_domain = SessionDomain(session_repository, application_repository, jwt_service)

def handler(event, context):
    """
    HTTP Handler for POST /init-session
    Stores cognito tokens and returns a session_id
    
    Args:
        event: API Gateway event containing POST body with tokens
        context: Lambda context
        
    Returns:
        API Gateway response with session_id
    """
    try:
        print("Init session request received:", json.dumps(event))
        
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
        cognito_tokens = request_data.get('tokens')
        application_id = request_data.get('application_id')
        
        if not cognito_tokens:
            return error_response(
                status_code=400,
                message="Missing required field: tokens",
                error_code="MISSING_TOKENS"
            )
        
        if not application_id:
            return error_response(
                status_code=400,
                message="Missing required field: application_id",
                error_code="MISSING_APPLICATION_ID"
            )
            
        # Extract device information from headers - only user agent for security
        headers = event.get('headers', {})
        user_agent = headers.get('User-Agent', '') or headers.get('user-agent', '')
        
        # Prepare device info dictionary - no IP address for security
        device_info = {
            'user_agent': user_agent
        }
        
        # Initialize session using domain layer
        try:
            session_id = session_domain.initialize_session(cognito_tokens, application_id, device_info)
        except ValueError as e:
            return error_response(
                status_code=401,
                message=str(e),
                error_code="SESSION_INIT_FAILED"
            )
        
        return success_response(
            data={
                "session_id": session_id,
                "application_id": application_id,
                "expires_in": 86400  # 24 hours in seconds
            },
            message="Session initialized successfully"
        )
        
    except Exception as e:
        print(f"Error in init session handler: {str(e)}")
        return error_response(
            status_code=500,
            message="Internal server error",
            error_code="INTERNAL_ERROR"
        ) 