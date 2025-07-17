import json
import os
import sys

# Add the parent directory to sys.path to allow importing from app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from services.aws.dynamodb_service import DynamoDBService
from services.repositories.application_repository import ApplicationRepository
from domains.application_domain import ApplicationDomain

# Initialize services and repositories
dynamodb_service = DynamoDBService()
application_repository = ApplicationRepository(dynamodb_service)
application_domain = ApplicationDomain(application_repository)

def handler(event, context):
    """
    PostSignIn Lambda trigger for Cognito.
    This function is triggered after a user successfully signs in.
    It checks if the user needs to authorize the application and handles consent flow.
    
    Args:
        event: The event from Cognito containing user attributes and client metadata
        context: Lambda context
        
    Returns:
        The event object to be passed back to Cognito
    """
    try:
        print("PostSignIn trigger received event:", json.dumps(event))
        
        # Extract user attributes from Cognito event
        user_attributes = event['request']['userAttributes']
        cognito_sub = user_attributes.get('sub')
        
        # Get application context from ClientMetadata (if available)
        client_metadata = event['request'].get('clientMetadata', {})
        application_name = client_metadata.get('application_name', '')
        
        print(f"PostSignIn - User: {cognito_sub}, Application: {application_name}")
        
        # If no application context, this is just a regular sign-in
        if not application_name:
            print("No application context found, allowing regular sign-in")
            return event
        
        # Find user by Cognito sub
        user = application_repository.find_user_by_sub(cognito_sub)
        if not user:
            print(f"User with sub {cognito_sub} not found in system")
            # This shouldn't happen if PostConfirmation worked properly
            return event
        
        user_id = user['PK']  # Extract user_id from the user record
        
        # Check if user has already authorized this application (jambyref.md simple schema)
        is_authorized = application_repository.check_app_user_authorization(application_name, user_id)
        
        if is_authorized:
            print(f"User {user_id} already authorized for application {application_name}")
            return event
        
        # User needs to authorize this application
        # Set a flag in the response that frontend can detect
        print(f"User {user_id} needs to authorize application {application_name}")
        
        # We can't directly redirect from PostSignIn trigger, but we can set custom attributes
        # The frontend will need to check for authorization status after login
        event['response']['claimsOverride'] = {
            'custom:needs_authorization': 'true',
            'custom:application_id': application_name
        }
        
        return event
        
    except Exception as e:
        print(f"Error in PostSignIn trigger: {str(e)}")
        # In case of error, we still return the event to not block the user sign-in
        return event 