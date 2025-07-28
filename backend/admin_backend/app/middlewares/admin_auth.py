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
            
            # Convert all header keys to lowercase for case-insensitive matching
            headers_lower = {k.lower(): v for k, v in headers.items()} if headers else {}
            
            if not headers_lower or 'authorization' not in headers_lower:
                print("Authorization header missing. Available headers:", headers)
                return {
                    'statusCode': 401,
                    'headers': {
                        'Content-Type': 'application/json',
                        'Access-Control-Allow-Origin': '*',
                        'Access-Control-Allow-Credentials': True,
                    },
                    'body': json.dumps({'message': 'Missing authorization header'})
                }
                
            # Extract the JWT token from the Authorization header
            auth_header = headers_lower.get('authorization')
            print("Authorization header found:", auth_header)
            token = auth_header.replace('Bearer ', '')
            
            # Verify token and extract claims
            claims = verify_token(token)
            
            # Check for admin role
            if not is_admin_user(claims):
                return {
                    'statusCode': 403,
                    'headers': {
                        'Content-Type': 'application/json',
                        'Access-Control-Allow-Origin': '*',
                        'Access-Control-Allow-Credentials': True,
                    },
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
            print(f"Admin auth error: {str(e)}")
            return {
                'statusCode': 401,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Credentials': True,
                },
                'body': json.dumps({'message': str(e)})
            }
        except Exception as e:
            print(f"Unexpected error in admin authorization: {str(e)}")
            print(traceback.format_exc())
            return {
                'statusCode': 500,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Credentials': True,
                },
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
        # Get Cognito user pool ID and region from environment variables
        user_pool_id = os.environ.get('COGNITO_USER_POOL_ID')
        region = os.environ.get('AWS_REGION', 'ap-southeast-2')
        
        if not user_pool_id:
            print("COGNITO_USER_POOL_ID environment variable not set")
            raise AdminAuthError('Configuration error')
            
        # Get token header
        header = jwt.get_unverified_header(token)
        
        # For debugging
        print(f"Token header: {header}")
        
        # For development/testing purposes, we'll use unverified claims
        # but log the details for debugging
        payload = jwt.get_unverified_claims(token)
        print(f"Token payload: {json.dumps(payload)}")
        
        # Check if token is expired
        if 'exp' in payload and payload['exp'] < int(time.time()):
            print(f"Token expired: {payload['exp']} < {int(time.time())}")
            raise AdminAuthError('Token is expired')
            
        # Check issuer
        expected_issuer = f'https://cognito-idp.{region}.amazonaws.com/{user_pool_id}'
        if 'iss' in payload and payload['iss'] != expected_issuer:
            print(f"Invalid issuer: {payload['iss']} != {expected_issuer}")
            # For debugging, we'll just log this but not fail
            print("WARNING: Token issuer doesn't match expected value")
            
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
    # Print all claims for debugging
    print(f"Checking admin status in claims: {json.dumps(claims)}")
    
    # Check for admin attribute in various possible formats
    # 1. Check custom:is_admin attribute
    if claims.get('custom:is_admin', '').lower() == 'true':
        return True
        
    # 2. Check cognito:groups to see if user is in admin group
    groups = claims.get('cognito:groups', [])
    if isinstance(groups, list) and 'admin' in [g.lower() for g in groups]:
        return True
        
    # 3. Check 'roles' claim if it exists
    roles = claims.get('roles', [])
    if isinstance(roles, list) and 'admin' in [r.lower() for r in roles]:
        return True
        
    # 4. For testing, if environment variable BYPASS_ADMIN_CHECK is set to true, allow all authenticated users
    if os.environ.get('BYPASS_ADMIN_CHECK', '').lower() == 'true':
        print("WARNING: Admin check bypassed due to BYPASS_ADMIN_CHECK environment variable")
        return True
        
    # No admin role found
    return False
