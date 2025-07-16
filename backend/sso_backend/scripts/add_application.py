#!/usr/bin/env python3
"""
Script to add application configuration to DynamoDB
"""

import boto3
from datetime import datetime

# DynamoDB setup
dynamodb = boto3.resource('dynamodb', region_name='ap-southeast-2')
main_table = dynamodb.Table('matt-cognito-hop-main')

def main():
    """Add application configuration"""
    
    print("🏗️  Adding Application Configuration to DynamoDB...")
    
    application_item = {
        "PK": "application-thegrind",
        "SK": "application", 
        "application_id": "thegrind",
        "name": "The Grind",
        "description": "Coffee empire application",
        "channels": [
            {
                "channel_id": "web",
                "return_url": "http://localhost:8080"
            }
        ],
        "created_at": datetime.now().isoformat()
    }
    
    try:
        main_table.put_item(Item=application_item)
        print(f"✅ Successfully added application: The Grind")
        print(f"   Channel: web")
        print(f"   Return URL: http://localhost:8080")
    except Exception as e:
        print(f"❌ Error adding application: {str(e)}")

if __name__ == "__main__":
    main() 