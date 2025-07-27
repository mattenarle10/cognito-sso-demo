import os
import json
from app.services.aws.cognito_admin_service import CognitoAdminService
from app.services.aws.dynamodb_service import DynamoDBService
from app.middlewares.admin_auth import admin_only

@admin_only
def handler(event, context):
    """
    Handler for deleting a user
    Removes user from Cognito User Pool and cleans up related DynamoDB records
    
    Args:
        event: API Gateway Lambda Proxy Input Format
        context: Lambda Context runtime methods and attributes
        
    Returns:
        API Gateway Lambda Proxy Output Format
    """
    try:
        # Extract user ID from path parameters
        user_id = event.get('pathParameters', {}).get('user_id')
        if not user_id:
            return {
                'statusCode': 400,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Credentials': True,
                },
                'body': json.dumps({'message': 'Missing user ID'})
            }
        
        # Parse request body for confirmation
        body = json.loads(event.get('body', '{}'))
        confirm = body.get('confirm', False)
        
        if not confirm:
            return {
                'statusCode': 400,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Credentials': True,
                },
                'body': json.dumps({
                    'message': 'Confirmation required',
                    'instructions': 'Set confirm: true in request body to confirm deletion'
                })
            }
        
        # Initialize services
        cognito_service = CognitoAdminService()
        dynamodb_service = DynamoDBService()
        
        # Delete user from Cognito
        cognito_success = cognito_service.delete_user(user_id)
        
        if not cognito_success:
            return {
                'statusCode': 500,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Credentials': True,
                },
                'body': json.dumps({'message': 'Failed to delete user from Cognito'})
            }
        
        # Clean up DynamoDB records
        db_user_id = f"user-{user_id}"
        
        # Delete user record
        dynamodb_service.delete_user_record(db_user_id)
        
        # Delete user authorizations
        dynamodb_service.delete_user_authorizations(db_user_id)
        
        # Delete user sessions
        dynamodb_service.delete_user_sessions(db_user_id)
        
        # Return success response
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Credentials': True,
            },
            'body': json.dumps({
                'message': 'User deleted successfully',
                'user_id': user_id
            })
        }
        
    except Exception as e:
        print(f"Error deleting user: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Credentials': True,
            },
            'body': json.dumps({
                'message': 'Error deleting user',
                'error': str(e)
            })
        }
