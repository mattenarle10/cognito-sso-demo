import json
import decimal
from decimal import Decimal

# Custom JSON encoder to handle Decimal objects
class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super(DecimalEncoder, self).default(obj)

def format_response(status_code, body):
    """
    Format a standard API Gateway response.
    
    Args:
        status_code (int): HTTP status code
        body (dict): Response body
        
    Returns:
        dict: Formatted response for API Gateway
    """
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Credentials': True
        },
        'body': json.dumps(body, cls=DecimalEncoder)
    }

def success_response(data=None, message=None):
    """
    Format a successful response.
    
    Args:
        data (dict, optional): Response data
        message (str, optional): Success message
        
    Returns:
        dict: Formatted success response
    """
    body = {
        'success': True
    }
    
    if data is not None:
        body['data'] = data
        
    if message is not None:
        body['message'] = message
        
    return format_response(200, body)

def error_response(status_code=400, message='An error occurred', error_code=None):
    """
    Format an error response.
    
    Args:
        status_code (int): HTTP status code
        message (str): Error message
        error_code (str, optional): Error code
        
    Returns:
        dict: Formatted error response
    """
    body = {
        'success': False,
        'message': message
    }
    
    if error_code is not None:
        body['error_code'] = error_code
        
    return format_response(status_code, body)
