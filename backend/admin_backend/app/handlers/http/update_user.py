import os
import json
from app.services.aws.cognito_admin_service import CognitoAdminService
from app.middlewares.admin_auth import admin_only

@admin_only
def handler(event, context):
    """
    Handler for updating user attributes
    Updates user information in Cognito User Pool
    
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
        if not body or not isinstance(body, dict):
            return {
                'statusCode': 400,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Credentials': True,
                },
                'body': json.dumps({'message': 'Invalid request body'})
            }
        
        # Extract attributes to update
        attributes = body.get('attributes', {})
        if not attributes:
            return {
                'statusCode': 400,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Credentials': True,
                },
                'body': json.dumps({'message': 'No attributes provided for update'})
            }
        
        # Validate attributes - prevent changing of critical attributes
        restricted_attributes = ['sub', 'email_verified', 'phone_number_verified', 'identities']
        for attr in restricted_attributes:
            if attr in attributes:
                return {
                    'statusCode': 400,
                    'headers': {
                        'Content-Type': 'application/json',
                        'Access-Control-Allow-Origin': '*',
                        'Access-Control-Allow-Credentials': True,
                    },
                    'body': json.dumps({
                        'message': f'Cannot update restricted attribute: {attr}',
                        'restricted_attributes': restricted_attributes
                    })
                }
        
        # Initialize Cognito service
        cognito_service = CognitoAdminService()
        
        # Update user attributes
        success = cognito_service.update_user_attributes(user_id, attributes)
        
        if not success:
            return {
                'statusCode': 500,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Credentials': True,
                },
                'body': json.dumps({'message': 'Failed to update user attributes'})
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
                'message': 'User attributes updated successfully',
                'updated_attributes': list(attributes.keys())
            })
        }
        
    except Exception as e:
        print(f"Error updating user: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Credentials': True,
            },
            'body': json.dumps({
                'message': 'Error updating user attributes',
                'error': str(e)
            })
        }
