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
    Lambda handler for DELETE /user-sessions/{session_id}
    Revokes a specific session or performs bulk operations
    
    Path parameters:
    - session_id: specific session to revoke OR 'all-others' for bulk revocation
    
    Body parameters (for bulk operations):
    - action: 'revoke_all_others' 
    - current_session_id: session to keep active
    """
    print("Revoke user session request received:", event)
    
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
        
        # Extract session_id from path parameters
        path_params = event.get('pathParameters') or {}
        session_id = path_params.get('session_id')
        
        if not session_id:
            return error_response("Missing session_id in path", 400)
        
        # Handle bulk operations
        if session_id == 'all-others':
            # Parse request body for bulk operations
            try:
                body = json.loads(event.get('body', '{}'))
                action = body.get('action')
                current_session_id = body.get('current_session_id')
                
                if action == 'revoke_all_others':
                    if not current_session_id:
                        return error_response("current_session_id required for bulk revocation", 400)
                    
                    revoked_count = session_domain.revoke_all_other_sessions(user_id, current_session_id)
                    
                    return success_response({
                        "message": f"Successfully revoked {revoked_count} sessions",
                        "revoked_count": revoked_count,
                        "action": "revoke_all_others"
                    })
                else:
                    return error_response("Invalid action for bulk operation", 400)
                    
            except json.JSONDecodeError:
                return error_response("Invalid JSON in request body", 400)
        else:
            # Handle single session revocation
            try:
                success = session_domain.revoke_session(session_id, user_id)
                
                if success:
                    return success_response({
                        "message": "Session revoked successfully",
                        "session_id": session_id,
                        "action": "revoke_single"
                    })
                else:
                    return error_response("Failed to revoke session", 500)
                    
            except ValueError as e:
                if "not found" in str(e):
                    return error_response("Session not found", 404)
                elif "unauthorized" in str(e):
                    return error_response("Unauthorized to revoke this session", 403)
                else:
                    return error_response(str(e), 400)
        
    except Exception as e:
        print(f"Error in revoke_user_session: {str(e)}")
        return error_response("Internal server error", 500) 