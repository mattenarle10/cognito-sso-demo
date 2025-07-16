import json
import os
import sys

# Add the parent directory to sys.path to allow importing from app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from services.aws.dynamodb_service import DynamoDBService
from services.repositories.session_repository import SessionRepository
from domains.session_domain import SessionDomain
from utils.response_formatter import success_response, error_response

# Initialize services and repositories
dynamodb_service = DynamoDBService()
session_repository = SessionRepository(dynamodb_service)
session_domain = SessionDomain(session_repository, None, None)  # only need session repo for this api

def handler(event, context):
    """
    HTTP Handler for GET /get-session
    Retrieves cognito tokens by session_id
    
    Args:
        event: API Gateway event containing query parameters
        context: Lambda context
        
    Returns:
        API Gateway response with token set
    """
    try:
        print("Get session request received:", json.dumps(event))
        
        # Extract query parameters
        query_params = event.get('queryStringParameters') or {}
        session_id = query_params.get('session_id')
        
        if not session_id:
            return error_response(
                status_code=400,
                message="Missing required parameter: session_id",
                error_code="MISSING_SESSION_ID"
            )
        
        # Get session tokens using domain layer
        session_data = session_domain.get_session_tokens(session_id)
        
        if not session_data:
            return error_response(
                status_code=404,
                message="Session not found or expired",
                error_code="SESSION_NOT_FOUND"
            )
        
        # Return the token set
        return success_response(
            data={
                "session_id": session_id,
                "user_id": session_data.get('user_id'),
                "application_id": session_data.get('application_id'),
                "tokens": {
                    "id_token": session_data.get('id_token'),
                    "access_token": session_data.get('access_token'),
                    "refresh_token": session_data.get('refresh_token'),
                    "token_type": session_data.get('token_type', 'Bearer'),
                    "expires_in": session_data.get('expires_in')
                },
                "expires_at": session_data.get('expires_at'),
                "created_at": session_data.get('created_at')
            },
            message="Session retrieved successfully"
        )
        
    except Exception as e:
        print(f"Error in get session handler: {str(e)}")
        return error_response(
            status_code=500,
            message="Internal server error",
            error_code="INTERNAL_ERROR"
        ) 