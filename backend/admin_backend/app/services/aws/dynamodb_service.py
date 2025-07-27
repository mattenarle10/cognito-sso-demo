import os
import boto3
from decimal import Decimal

class DynamoDBService:
    """
    Service for DynamoDB operations in admin backend
    Handles access to the main table for user-related operations
    """
    
    def __init__(self):
        """Initialize DynamoDB service with table names from environment"""
        self.dynamodb = boto3.resource('dynamodb')
        self.main_table_name = os.environ.get('MAIN_TABLE', 'matt-cognito-hop-main')
        self.main_table = self.dynamodb.Table(self.main_table_name)
    
    def get_user_by_id(self, user_id):
        """
        Get user record by user ID
        
        Args:
            user_id (str): The user ID (like user-9fef7f58)
            
        Returns:
            dict: User record if found, None otherwise
        """
        try:
            response = self.main_table.get_item(
                Key={
                    'PK': user_id,
                    'SK': 'user'
                }
            )
            return response.get('Item')
        except Exception as e:
            print(f"Error getting user {user_id}: {str(e)}")
            return None
    
    def get_user_applications(self, user_id):
        """
        Get application authorizations for a user
        
        Args:
            user_id (str): The user ID
            
        Returns:
            list: List of application authorizations
        """
        try:
            response = self.main_table.query(
                KeyConditionExpression=boto3.dynamodb.conditions.Key('PK').eq(user_id) & 
                                      boto3.dynamodb.conditions.Key('SK').begins_with('application-')
            )
            return response.get('Items', [])
        except Exception as e:
            print(f"Error querying applications for user {user_id}: {str(e)}")
            return []
    
    def delete_user_record(self, user_id):
        """
        Delete user record from DynamoDB
        
        Args:
            user_id (str): The user ID
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            self.main_table.delete_item(
                Key={
                    'PK': user_id,
                    'SK': 'user'
                }
            )
            return True
        except Exception as e:
            print(f"Error deleting user record {user_id}: {str(e)}")
            return False
    
    def delete_user_authorizations(self, user_id):
        """
        Delete all application authorizations for a user
        
        Args:
            user_id (str): The user ID
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # First, query to get all authorizations
            authorizations = self.get_user_applications(user_id)
            
            # Delete each authorization
            for auth in authorizations:
                self.main_table.delete_item(
                    Key={
                        'PK': auth['PK'],
                        'SK': auth['SK']
                    }
                )
            return True
        except Exception as e:
            print(f"Error deleting authorizations for user {user_id}: {str(e)}")
            return False
            
    def delete_user_sessions(self, user_id):
        """
        Delete all sessions for a user
        
        Args:
            user_id (str): The user ID
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Query to find all sessions for this user
            response = self.main_table.query(
                KeyConditionExpression=boto3.dynamodb.conditions.Key('PK').begins_with('session-') & 
                                      boto3.dynamodb.conditions.Key('SK').eq(user_id)
            )
            
            # Delete each session
            for session in response.get('Items', []):
                self.main_table.delete_item(
                    Key={
                        'PK': session['PK'],
                        'SK': session['SK']
                    }
                )
            return True
        except Exception as e:
            print(f"Error deleting sessions for user {user_id}: {str(e)}")
            return False
