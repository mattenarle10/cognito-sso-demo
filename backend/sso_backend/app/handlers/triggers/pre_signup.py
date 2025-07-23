import json
import os
import sys

# Add the parent directory to sys.path to allow importing from app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from services.aws.dynamodb_service import DynamoDBService
from services.repositories.user_repository import UserRepository
from services.repositories.application_repository import ApplicationRepository
from domains.user_domain import UserDomain
import uuid

# Initialize services and repositories
dynamodb_service = DynamoDBService()
user_repository = UserRepository(dynamodb_service)
application_repository = ApplicationRepository(dynamodb_service)
user_domain = UserDomain(user_repository, application_repository)

def create_uuid():
    """Generate a unique identifier for users"""
    return f"user-{str(uuid.uuid4())[:8]}"

def handler(event, context):
    """
    PreSignUp Lambda trigger for Cognito.
    This function is triggered before a user signs up.
    It handles different signup scenarios including social providers.
    
    Args:
        event: The event from Cognito containing user attributes
        context: Lambda context
        
    Returns:
        The event object to be passed back to Cognito
    """
    try:
        print("PreSignUp trigger received event:", json.dumps(event))
        
        # Only auto-confirm users for external providers (social logins)
        if event["triggerSource"] == "PreSignUp_ExternalProvider":
            print("External provider signup detected, auto-confirming user.")
            event["response"]["autoConfirmUser"] = True
        else:
            print("Regular signup flow detected, NOT auto-confirming user.")
            event["response"]["autoConfirmUser"] = False
        
        # If the signup was from AdminCreateUser, just return
        if event["triggerSource"] == "PreSignUp_AdminCreateUser":
            print("AdminCreateUser flow detected, allowing without changes")
            return event

        # Handle social provider signup (Google, Facebook, etc.)
        if event["triggerSource"] == "PreSignUp_ExternalProvider":
            print("External provider signup detected")
            
            # Check for client_metadata
            client_metadata = event.get("request", {}).get("clientMetadata", {})
            print(f"Client metadata received: {json.dumps(client_metadata)}")
            
            # Auto-verify email for social logins
            event["response"]["autoVerifyEmail"] = True
            event["request"]["userAttributes"]["email_verified"] = "true"
            
            # Extract email from user attributes
            user_email = event["request"]["userAttributes"]["email"]
            print(f"Social login with email: {user_email}")
            
            # Set a placeholder phone number if not provided
            if "phone_number" not in event["request"]["userAttributes"] or not event["request"]["userAttributes"]["phone_number"]:
                print("Phone number not provided, setting placeholder")
                event["request"]["userAttributes"]["phone_number"] = "+00000000000"
                # Mark user as needing profile completion
                event["request"]["userAttributes"]["custom:needs_profile_completion"] = "true"
                print("User marked as needing profile completion")
                
            # Always auto-confirm users from social providers
            event["response"]["autoConfirmUser"] = True
            print("Auto-confirming social provider user")
            
            # Check if there's an existing user with this email
            existing_user = user_repository.find_user_by_email(user_email)
            
            # Extract provider information
            provider_name = event["userName"].split("_", 1)[0]
            provider_id = event["userName"].split("_", 1)[1]
            
            # Format provider name for display
            if provider_name.lower() == "google":
                formatted_provider = "Google"
            elif provider_name.lower() == "facebook":
                formatted_provider = "Facebook"
            else:
                formatted_provider = provider_name.title()
                
            print(f"Provider: {formatted_provider}, ID: {provider_id}")
            
            # Prepare provider data structure
            provider_data = {
                "new": {
                    "id": provider_id,
                    "provider_name": formatted_provider
                }
            }
            
            # If there's an existing user with this email
            if existing_user:
                print(f"Found existing user with email {user_email}")
                
                # Get the user_id from the existing user
                user_id = existing_user.get("PK")
                
                # Link the social provider to the existing user
                user_repository.link_social_provider(existing_user, formatted_provider, provider_id)
                
                # Use the existing user's ID for this login
                event["userName"] = user_id
                print(f"Linked social account to existing user: {user_id}")
                
                # Set a custom attribute to indicate this is a linked account
                if "custom:is_linked_account" not in event["request"]["userAttributes"]:
                    event["request"]["userAttributes"]["custom:is_linked_account"] = "true"
            
            # If no existing user, create a new one
            else:
                print(f"No existing user found for email {user_email}, creating new user")
                
                # Generate a username for the new user
                event["request"]["userAttributes"]["user_name"] = create_uuid()
                
                # We'll let post_confirmation handle the actual user creation
                print(f"New user will be created with ID: {event['request']['userAttributes']['user_name']}")
        
        # Handle regular signup
        elif event["triggerSource"] == "PreSignUp_SignUp":
            print("Regular signup flow detected")
            
            # Check for duplicate email
            user_email = event["request"]["userAttributes"]["email"]
            existing_user = user_repository.find_user_by_email(user_email)
            
            if existing_user:
                print(f"User with email {user_email} already exists")
                raise Exception("A user with this email already exists")
            
        
        return event
        
    except Exception as e:
        print(f"Error in PreSignUp trigger: {str(e)}")
        # Re-raise the exception to prevent signup if there's an error
        raise e
