import os
import boto3
from datetime import datetime

class DynamoDBService:
    """
    Service class for DynamoDB operations.
    Provides methods to interact with DynamoDB tables.
    """
    
    def __init__(self):
        """Initialize the DynamoDB service with the main table name from environment variables."""
        self.dynamodb = boto3.resource('dynamodb')
        self.main_table_name = os.environ.get('MAIN_TABLE', 'matt-cognito-hop-main')
        self.main_table = self.dynamodb.Table(self.main_table_name)
    
    def put_item(self, item):
        """
        Put an item into the main table.
        
        Args:
            item (dict): The item to put into the table
            
        Returns:
            dict: The response from DynamoDB
        """
        return self.main_table.put_item(Item=item)
    
    def get_item(self, key):
        """
        Get an item from the main table.
        
        Args:
            key (dict): The key to get the item
            
        Returns:
            dict: The item from DynamoDB
        """
        response = self.main_table.get_item(Key=key)
        return response.get('Item')
    
    def update_item(self, key, update_expression, expression_attribute_values, expression_attribute_names=None):
        """
        Update an item in the main table.
        
        Args:
            key (dict): The key of the item to update
            update_expression (str): The update expression
            expression_attribute_values (dict): Values for the expression
            expression_attribute_names (dict): Names for the expression (optional)
            
        Returns:
            dict: The response from DynamoDB
        """
        params = {
            'Key': key,
            'UpdateExpression': update_expression,
            'ExpressionAttributeValues': expression_attribute_values,
            'ReturnValues': 'UPDATED_NEW'
        }
        
        if expression_attribute_names:
            params['ExpressionAttributeNames'] = expression_attribute_names
            
        return self.main_table.update_item(**params)
    
    def query(self, key_condition_expression, expression_attribute_values=None, expression_attribute_names=None):
        """
        Query items from the main table.
        
        Args:
            key_condition_expression (str): The key condition expression
            expression_attribute_values (dict): The expression attribute values
            expression_attribute_names (dict): The expression attribute names
            
        Returns:
            list: The items from DynamoDB
        """
        query_params = {
            'KeyConditionExpression': key_condition_expression
        }
        
        if expression_attribute_values:
            query_params['ExpressionAttributeValues'] = expression_attribute_values
            
        if expression_attribute_names:
            query_params['ExpressionAttributeNames'] = expression_attribute_names
            
        response = self.main_table.query(**query_params)
        return response.get('Items', [])
    
    def query_index(self, params):
        """
        Query items from a GSI.
        
        Args:
            params (dict): Query parameters including IndexName and KeyConditionExpression
            
        Returns:
            dict: The response from DynamoDB including Items
        """
        # Make sure we're using the main table
        response = self.main_table.query(**params)
        return response
        
    def scan(self, params):
        """
        Scan the main table with optional filters.
        
        Args:
            params (dict): Scan parameters including FilterExpression and ExpressionAttributeValues
            
        Returns:
            list: The items from DynamoDB
        """
        response = self.main_table.scan(**params)
        return response.get('Items', [])
