#!/usr/bin/env python3
import boto3
import json
from datetime import datetime

"""
Script to create admin-portal authorization for admin user
"""

# Constants
ADMIN_USER_ID = "user-31aea894-3ce6-4896-b6cb-5a32fd2b6599"
APPLICATION_ID = "admin-portal"
TABLE_NAME = "matt-cognito-hop-main"

# Initialize DynamoDB client
dynamodb = boto3.resource('dynamodb', region_name='ap-southeast-2')
table = dynamodb.Table(TABLE_NAME)

def create_app_user_relationship():
    """Create application-user relationship record in DynamoDB"""
    
    # Current timestamp
    timestamp = datetime.now().isoformat()
    
    # Create application-user relationship record
    app_user_item = {
        "PK": f"application-{APPLICATION_ID}",
        "SK": ADMIN_USER_ID,
        "application_id": APPLICATION_ID,
        "user_id": ADMIN_USER_ID,
        "created_at": timestamp
    }
    
    # Save to DynamoDB
    try:
        table.put_item(Item=app_user_item)
        print(f"✅ Successfully created relationship between admin user and {APPLICATION_ID}")
        print(f"Item: {json.dumps(app_user_item, indent=2)}")
    except Exception as e:
        print(f"❌ Error creating relationship: {e}")

if __name__ == "__main__":
    print(f"Creating admin authorization for user ID {ADMIN_USER_ID}...")
    create_app_user_relationship()
