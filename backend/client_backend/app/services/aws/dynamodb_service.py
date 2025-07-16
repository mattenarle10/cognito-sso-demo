import os
import boto3

class DynamoDBService:
    """
    service for dynamodb operations in client backend
    handles both orders table and main table access
    """
    
    def __init__(self):
        """initialize dynamodb service with table names from environment"""
        self.dynamodb = boto3.resource('dynamodb')
        self.orders_table_name = os.environ.get('ORDERS_TABLE', 'matt-cognito-hop-orders')
        self.main_table_name = os.environ.get('MAIN_TABLE', 'matt-cognito-hop-main')
        self.orders_table = self.dynamodb.Table(self.orders_table_name)
        self.main_table = self.dynamodb.Table(self.main_table_name)
    
    def query_orders_by_user(self, user_id):
        """
        query orders table for a specific user
        
        args:
            user_id (str): the user id (like user-9fef7f58)
            
        returns:
            list: list of order items for the user
        """
        try:
            response = self.orders_table.query(
                KeyConditionExpression=boto3.dynamodb.conditions.Key('PK').eq(user_id)
            )
            return response.get('Items', [])
        except Exception as e:
            print(f"error querying orders for user {user_id}: {str(e)}")
            return []
    
    def scan_users_by_sub(self, cognito_sub):
        """
        find user by cognito sub in main table
        note: in production, use gsi. for now, scan is ok with minimal data
        
        args:
            cognito_sub (str): cognito user sub
            
        returns:
            dict: user item if found, none otherwise
        """
        try:
            response = self.main_table.scan(
                FilterExpression=boto3.dynamodb.conditions.Attr('SK').eq('user') & 
                               boto3.dynamodb.conditions.Attr('sub').eq(cognito_sub)
            )
            
            items = response.get('Items', [])
            return items[0] if items else None
            
        except Exception as e:
            print(f"error finding user by sub {cognito_sub}: {str(e)}")
            return None 