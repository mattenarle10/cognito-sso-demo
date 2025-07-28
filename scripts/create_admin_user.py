#!/usr/bin/env python3
"""
Script to create an admin user in Cognito and update DynamoDB accordingly.
Admin users have the custom:is_admin attribute set to "true" in Cognito.
"""

import boto3
import uuid
import json
import time
from datetime import datetime
import argparse

# Parse command-line arguments
parser = argparse.ArgumentParser(description='Create an admin user in Cognito SSO system')
parser.add_argument('--email', required=True, help='Admin user email address')
parser.add_argument('--password', required=True, help='Admin user password')
parser.add_argument('--first_name', required=True, help='Admin user first name')
parser.add_argument('--last_name', required=True, help='Admin user last name')
parser.add_argument('--phone_number', required=True, help='Admin user phone number (format: +xxxxxxxxxxx)')
parser.add_argument('--gender', choices=['Male', 'Female'], default='Male', help='Admin user gender')
args = parser.parse_args()

# AWS Configuration - replace with your values if different
REGION = 'ap-southeast-2'  
USER_POOL_ID = 'ap-southeast-2_TbDhVxp4R'
APP_CLIENT_ID = '4b3r9o59eh1n9m61fo66ji9mvd'
MAIN_TABLE = 'matt-cognito-hop-main'

# Initialize AWS clients
cognito = boto3.client('cognito-idp', region_name=REGION)
dynamodb = boto3.client('dynamodb', region_name=REGION)

def create_admin_user():
    """Create an admin user in Cognito with the custom:is_admin attribute."""
    try:
        # Generate a user ID for consistency between Cognito and DynamoDB
        user_id = str(uuid.uuid4())
        
        print(f"Creating admin user {args.email} in Cognito...")
        
        # Create user in Cognito
        cognito.admin_create_user(
            UserPoolId=USER_POOL_ID,
            Username=args.email,
            UserAttributes=[
                {'Name': 'email', 'Value': args.email},
                {'Name': 'email_verified', 'Value': 'true'},
                {'Name': 'name', 'Value': f"{args.first_name} {args.last_name}"},
                {'Name': 'given_name', 'Value': args.first_name},
                {'Name': 'family_name', 'Value': args.last_name},
                {'Name': 'phone_number', 'Value': args.phone_number},
                {'Name': 'phone_number_verified', 'Value': 'true'},
                {'Name': 'custom:gender', 'Value': args.gender},
                {'Name': 'custom:is_admin', 'Value': 'true'},

            ],
            MessageAction='SUPPRESS',  # Don't send welcome email
            TemporaryPassword=args.password
        )
        
        # Set the permanent password
        cognito.admin_set_user_password(
            UserPoolId=USER_POOL_ID,
            Username=args.email,
            Password=args.password,
            Permanent=True
        )
        
        print(f"Successfully created admin user in Cognito!")
        
        # Add user to DynamoDB
        add_user_to_dynamodb(user_id)
        
        return user_id
    
    except Exception as e:
        print(f"Error creating admin user: {str(e)}")
        return None

def add_user_to_dynamodb(user_id):
    """Add the admin user to DynamoDB."""
    try:
        print(f"Adding user {args.email} to DynamoDB...")
        
        # Current timestamp in ISO format
        timestamp = datetime.utcnow().isoformat() + 'Z'
        
        # Create user record in DynamoDB
        dynamodb.put_item(
            TableName=MAIN_TABLE,
            Item={
                'PK': {'S': f"user-{user_id}"},
                'SK': {'S': "profile"},
                'email': {'S': args.email},
                'given_name': {'S': args.first_name},
                'family_name': {'S': args.last_name},
                'name': {'S': f"{args.first_name} {args.last_name}"},
                'phone_number': {'S': args.phone_number},
                'gender': {'S': args.gender},
                'is_admin': {'S': 'true'},
                'created_at': {'S': timestamp},
                'updated_at': {'S': timestamp}
            }
        )
        
        print(f"Successfully added user to DynamoDB!")
    
    except Exception as e:
        print(f"Error adding user to DynamoDB: {str(e)}")

if __name__ == "__main__":
    user_id = create_admin_user()
    
    if user_id:
        print("\n========== SUCCESS ==========")
        print(f"Admin user created successfully!")
        print(f"Email: {args.email}")
        print(f"User ID: {user_id}")
        print(f"Admin Status: true")
        print("============================")
        print("\nYou can now log in to the SSO portal with these credentials.")
        print("You'll be automatically redirected to the Admin Portal after login.")
    else:
        print("\nFailed to create admin user. Please check the error messages above.")
