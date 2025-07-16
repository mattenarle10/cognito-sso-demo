import json
import os
import sys

# Add the parent directory to sys.path to allow importing from app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from services.aws.dynamodb_service import DynamoDBService
from services.repositories.application_repository import ApplicationRepository
from domains.application_domain import ApplicationDomain
from utils.response_formatter import success_response, error_response

# Initialize services and repositories
dynamodb_service = DynamoDBService()
application_repository = ApplicationRepository(dynamodb_service)
application_domain = ApplicationDomain(application_repository)

def handler(event, context):
    """
    HTTP Handler for GET /validate-app-channel
    Validates if application_id + channel_id combination exists
    
    Args:
        event: API Gateway event containing query parameters
        context: Lambda context
        
    Returns:
        API Gateway response with validation result
    """
    try:
        print("Validate app channel request received:", json.dumps(event))
        
        # Extract query parameters
        query_params = event.get('queryStringParameters') or {}
        application_id = query_params.get('application_id')
        channel_id = query_params.get('channel_id')
        
        # Validate required parameters
        if not application_id or not channel_id:
            return error_response(
                status_code=400,
                message="Missing required parameters: application_id and channel_id",
                error_code="MISSING_PARAMETERS"
            )
        
        # Validate app and channel using domain layer
        is_valid, return_url = application_domain.validate_app_channel(application_id, channel_id)
        
        if is_valid:
            return success_response(
                data={
                    "valid": True,
                    "application_id": application_id,
                    "channel_id": channel_id,
                    "return_url": return_url
                },
                message="Valid application and channel combination"
            )
        else:
            return error_response(
                status_code=404,
                message="Invalid application or channel combination",
                error_code="INVALID_APP_CHANNEL"
            )
        
    except Exception as e:
        print(f"Error in validate app channel handler: {str(e)}")
        return error_response(
            status_code=500,
            message="Internal server error",
            error_code="INTERNAL_ERROR"
        ) 