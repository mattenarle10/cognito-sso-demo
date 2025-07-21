import json
import sys
import os

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from utils.response_formatter import success_response, error_response
from services.auth.jwt_service import JWTService
from services.aws.dynamodb_service import DynamoDBService
from services.repositories.session_repository import SessionRepository
from services.repositories.application_repository import ApplicationRepository
from domains.session_domain import SessionDomain

# Initialize services and domain
jwt_service = JWTService()
dynamodb_service = DynamoDBService()
session_repository = SessionRepository(dynamodb_service)
application_repository = ApplicationRepository(dynamodb_service)
session_domain = SessionDomain(session_repository, application_repository, jwt_service)

def lambda_handler(event, context):
    """
    Lambda handler for GET /user-sessions
    Returns all sessions for the authenticated user
    
    Query parameters:
    - include_expired: 'true' to include expired sessions (default: false)
    """
    print("Get user sessions request received:", event)
    
    try:
        # Extract authorization header
        headers = event.get('headers', {})
        auth_header = headers.get('authorization') or headers.get('Authorization')
        
        if not auth_header or not auth_header.startswith('Bearer '):
            return error_response("Missing or invalid authorization header", 401)
        
        id_token = auth_header.replace('Bearer ', '')
        
        # Validate token and extract user info
        try:
            user_info = jwt_service.extract_user_info(id_token)
            cognito_sub = user_info['sub']
        except ValueError as e:
            print(f"Token validation failed: {str(e)}")
            return error_response("Invalid or expired token", 401)
        
        # Find user by cognito sub
        user = application_repository.find_user_by_sub(cognito_sub)
        if not user:
            return error_response("User not found", 404)
        
        user_id = user['PK']
        
        # Parse query parameters
        query_params = event.get('queryStringParameters') or {}
        include_expired = query_params.get('include_expired', 'false').lower() == 'true'
        
        # Get user sessions
        sessions_data = session_domain.get_user_sessions(user_id, include_expired)
        
        # Prepare response data
        response_data = {
            "user_id": user_id,
            "sessions": sessions_data,
            "summary": {
                "active_count": len(sessions_data['active']),
                "expired_count": len(sessions_data['expired']),
                "total_count": len(sessions_data['active']) + len(sessions_data['expired'])
            }
        }
        
        return success_response(response_data)
        
    except Exception as e:
        print(f"Error in get_user_sessions: {str(e)}")
        return error_response("Internal server error", 500) 