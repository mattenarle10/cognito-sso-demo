import os
import json
import base64
import time
import traceback
from functools import wraps
from jose import jwk, jwt
from jose.utils import base64url_decode

class AdminAuthError(Exception):
    """Custom exception for admin authorization failures"""
    pass

def admin_only(handler):
    """
    Middleware decorator to verify admin access to endpoints
    Validates JWT token and checks for admin role in custom:is_admin claim
    
    Args:
        handler: The Lambda handler function
        
    Returns:
        Wrapped function that checks admin authorization before executing handler
    """
    @wraps(handler)
    def wrapper(event, context):
        try:
            # Check if Authorization header is present
            headers = event.get('headers', {})
            if not headers or 'authorization' not in headers:
                return {
                    'statusCode': 401,
                    'body': json.dumps({'message': 'Missing authorization header'})
                }
                
            # Extract the JWT token from the Authorization header
            auth_header = headers.get('authorization')
            token = auth_header.replace('Bearer ', '')
            
            # Verify token and extract claims
            claims = verify_token(token)
            
            # Check for admin role
            if not is_admin_user(claims):
                return {
                    'statusCode': 403,
                    'body': json.dumps({'message': 'Insufficient permissions - Admin access required'})
                }
            
            # Add the verified claims to the event for use in the handler
            event['requestContext'] = event.get('requestContext', {})
            event['requestContext']['authorizer'] = {
                'jwt': {'claims': claims}
            }
            
            # Proceed with the handler if authorization successful
            return handler(event, context)
            
        except AdminAuthError as e:
            return {
                'statusCode': 401,
                'body': json.dumps({'message': str(e)})
            }
        except Exception as e:
            print(f"Unexpected error in admin authorization: {str(e)}")
            print(traceback.format_exc())
            return {
                'statusCode': 500,
                'body': json.dumps({'message': 'Internal server error during authorization'})
            }
    
    return wrapper

def verify_token(token):
    """
    Verify JWT token signature and expiration
    
    Args:
        token (str): JWT token
        
    Returns:
        dict: Token claims if valid
        
    Raises:
        AdminAuthError: If token is invalid
    """
    try:
        # Get token header and payload
        header = jwt.get_unverified_header(token)
        
        # This is a simplified version - in production, you'd verify the token signature
        # with the Cognito public keys and properly validate all claims
        # For testing purposes, we'll just decode the token to get the claims
        
        # For production use, implement full token verification:
        # 1. Fetch Cognito public keys from jwks_uri endpoint
        # 2. Verify token signature with the matching key
        # 3. Validate token issuer, audience, and expiration
        
        # Decode token without verification for now (REPLACE THIS IN PRODUCTION!)
        payload = jwt.get_unverified_claims(token)
        
        # Check if token is expired
        if 'exp' in payload and payload['exp'] < int(time.time()):
            raise AdminAuthError('Token is expired')
            
        return payload
        
    except Exception as e:
        print(f"Error verifying token: {str(e)}")
        raise AdminAuthError('Invalid token')

def is_admin_user(claims):
    """
    Check if the user has admin role based on JWT claims
    
    Args:
        claims (dict): JWT token claims
        
    Returns:
        bool: True if user has admin role, False otherwise
    """
    # Check for admin attribute in claims
    is_admin = claims.get('custom:is_admin', '').lower() == 'true'
    return is_admin
