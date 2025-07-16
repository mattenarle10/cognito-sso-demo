import json
import os
import sys

# Add the parent directory to sys.path to allow importing from app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from services.aws.dynamodb_service import DynamoDBService
from services.repositories.order_repository import OrderRepository
from services.auth.jwt_service import JWTService
from domains.order_domain import OrderDomain
from utils.response_formatter import success_response, error_response

# Initialize services and repositories
dynamodb_service = DynamoDBService()
order_repository = OrderRepository(dynamodb_service)
jwt_service = JWTService()
order_domain = OrderDomain(order_repository, jwt_service)

def handler(event, context):
    """
    HTTP Handler for GET /orders
    Returns all orders for authenticated user
    
    Args:
        event: API Gateway event containing headers
        context: Lambda context
        
    Returns:
        API Gateway response with user's orders
    """
    try:
        print("Get orders request received:", json.dumps(event))
        
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
        
        # Get user orders using domain layer
        try:
            orders = order_domain.get_user_orders(id_token)
        except ValueError as e:
            return error_response(
                status_code=401,
                message=str(e),
                error_code="UNAUTHORIZED"
            )
        
        return success_response(
            data={
                "orders": orders,
                "total_orders": len(orders)
            },
            message="Orders retrieved successfully"
        )
        
    except Exception as e:
        print(f"Error in get orders handler: {str(e)}")
        return error_response(
            status_code=500,
            message="Internal server error",
            error_code="INTERNAL_ERROR"
        ) 