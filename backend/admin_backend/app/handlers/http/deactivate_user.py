import os
import json
from app.services.aws.cognito_admin_service import CognitoAdminService
from app.middlewares.admin_auth import admin_only

@admin_only
def handler(event, context):
    """
    Handler for deactivating a user account
    Disables the user in Cognito User Pool
    
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
        
        # Parse request body
        body = json.loads(event.get('body', '{}'))
        
        # Check for deactivation or reactivation action
        action = body.get('action', 'deactivate').lower()
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
                    'instructions': 'Set confirm: true in request body to confirm user account status change'
                })
            }
        
        # Initialize Cognito service
        cognito_service = CognitoAdminService()
        
        success = False
        action_performed = ""
        
        # Handle different actions
        if action == 'deactivate':
            success = cognito_service.deactivate_user(user_id)
            action_performed = "deactivated"
        elif action == 'activate':
            success = cognito_service.activate_user(user_id)
            action_performed = "activated"
        else:
            return {
                'statusCode': 400,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Credentials': True,
                },
                'body': json.dumps({
                    'message': 'Invalid action',
                    'allowed_actions': ['deactivate', 'activate']
                })
            }
        
        if not success:
            return {
                'statusCode': 500,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Credentials': True,
                },
                'body': json.dumps({
                    'message': f'Failed to {action} user account'
                })
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
                'message': f'User account {action_performed} successfully',
                'user_id': user_id,
                'action': action
            })
        }
        
    except Exception as e:
        print(f"Error changing user account status: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Credentials': True,
            },
            'body': json.dumps({
                'message': 'Error changing user account status',
                'error': str(e)
            })
        }
