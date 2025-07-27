import os
import json
from app.services.aws.cognito_admin_service import CognitoAdminService
from app.services.aws.dynamodb_service import DynamoDBService
from app.middlewares.admin_auth import admin_only

@admin_only
def handler(event, context):
    """
    Handler for getting detailed information for a specific user
    Combines data from both Cognito User Pool and DynamoDB
    
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
        
        # Initialize services
        cognito_service = CognitoAdminService()
        dynamodb_service = DynamoDBService()
        
        # Get user from Cognito
        user_data = cognito_service.get_user(user_id)
        
        if not user_data:
            return {
                'statusCode': 404,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Credentials': True,
                },
                'body': json.dumps({'message': 'User not found'})
            }
        
        # Get additional user data from DynamoDB
        dynamodb_user = dynamodb_service.get_user_by_id(f"user-{user_id}")
        
        # Get user's authorized applications
        user_applications = dynamodb_service.get_user_applications(f"user-{user_id}")
        
        # Combine data
        complete_user_data = {
            **user_data,
            'dynamodb_data': dynamodb_user if dynamodb_user else {},
            'authorized_applications': [
                {
                    'application_id': app.get('SK', '').replace('application-', ''),
                    'authorized_at': app.get('authorized_at', ''),
                    'channels': app.get('channels', [])
                } 
                for app in user_applications
            ]
        }
        
        # Return success response
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Credentials': True,
            },
            'body': json.dumps(complete_user_data)
        }
        
    except Exception as e:
        print(f"Error getting user: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Credentials': True,
            },
            'body': json.dumps({
                'message': 'Error getting user details',
                'error': str(e)
            })
        }
