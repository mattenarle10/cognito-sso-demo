import os
import json
from app.services.aws.cognito_admin_service import CognitoAdminService
from app.middlewares.admin_auth import admin_only

@admin_only
def handler(event, context):
    """
    Handler for forcing a user to reset password on next login
    
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
                    'instructions': 'Set confirm: true in request body to confirm password reset'
                })
            }
        
        # Initialize Cognito service
        cognito_service = CognitoAdminService()
        
        # Force password reset
        success = cognito_service.force_password_reset(user_id)
        
        if not success:
            return {
                'statusCode': 500,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Credentials': True,
                },
                'body': json.dumps({'message': 'Failed to initiate password reset'})
            }
        
        # Return success response
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Credentials': True,
            },
            'body': json.dumps({
                'message': 'Password reset initiated successfully',
                'user_id': user_id,
                'status': 'User will be prompted to reset password on next login'
            })
        }
        
    except Exception as e:
        print(f"Error initiating password reset: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Credentials': True,
            },
            'body': json.dumps({
                'message': 'Error initiating password reset',
                'error': str(e)
            })
        }
