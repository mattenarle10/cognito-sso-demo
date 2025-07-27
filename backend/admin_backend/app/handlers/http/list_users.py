import os
import json
from app.services.aws.cognito_admin_service import CognitoAdminService
from app.middlewares.admin_auth import admin_only

@admin_only
def handler(event, context):
    """
    Handler for listing all users with optional filtering and pagination
    
    Args:
        event: API Gateway Lambda Proxy Input Format
        context: Lambda Context runtime methods and attributes
        
    Returns:
        API Gateway Lambda Proxy Output Format
    """
    try:
        # Parse query string parameters
        query_params = event.get('queryStringParameters', {}) or {}
        limit = int(query_params.get('limit', 25))
        pagination_token = query_params.get('pagination_token')
        filter_expr = query_params.get('filter')
        
        # Initialize Cognito service
        cognito_service = CognitoAdminService()
        
        # Get users from Cognito
        result = cognito_service.list_users(
            limit=limit, 
            pagination_token=pagination_token, 
            filter_expr=filter_expr
        )
        
        # Return success response with users and pagination token
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Credentials': True,
            },
            'body': json.dumps({
                'users': result['users'],
                'pagination': {
                    'next_token': result.get('pagination_token')
                },
                'total_count': len(result['users'])
            })
        }
        
    except Exception as e:
        print(f"Error listing users: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Credentials': True,
            },
            'body': json.dumps({
                'message': 'Error listing users',
                'error': str(e)
            })
        }
