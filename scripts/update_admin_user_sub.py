#!/usr/bin/env python3
import boto3
import json

"""
Script to update the admin user record with the Cognito sub ID
"""

# Constants
ADMIN_USER_ID = "user-31aea894-3ce6-4896-b6cb-5a32fd2b6599"
TABLE_NAME = "matt-cognito-hop-main"

# Initialize DynamoDB client
dynamodb = boto3.resource('dynamodb', region_name='ap-southeast-2')
table = dynamodb.Table(TABLE_NAME)

def get_admin_cognito_sub():
    """
    Get admin user's Cognito sub ID.
    In a real scenario, you would get this from Cognito.
    For now, let's simulate by asking the user for the sub.
    """
    print("\nTo update the admin user, we need the Cognito sub ID.")
    print("You can get this from the Cognito User Pool console or by exporting user attributes.")
    cognito_sub = input("Please enter the admin user's Cognito sub ID: ")
    return cognito_sub.strip()

def update_admin_user_with_sub(cognito_sub):
    """Update the admin user record with the Cognito sub ID"""
    
    try:
        # First, get the current user record
        response = table.get_item(Key={
            "PK": ADMIN_USER_ID,
            "SK": "user"
        })
        
        if 'Item' not in response:
            # Try to get the profile record if user record doesn't exist
            response = table.get_item(Key={
                "PK": ADMIN_USER_ID,
                "SK": "profile"
            })
            
            if 'Item' not in response:
                print(f"❌ Error: Admin user record not found with ID {ADMIN_USER_ID}")
                return
            
            # Create user record based on profile
            item = response['Item']
            user_item = {
                "PK": ADMIN_USER_ID,
                "SK": "user",
                "user_id": ADMIN_USER_ID,
                "email": item.get("email", "matthew.enarle@ecloudvalley.com"),
                "is_admin": True,
                "sub": cognito_sub  # Add the sub
            }
            
            # Add additional fields from profile if available
            if "name" in item:
                user_item["name"] = item["name"]
            if "given_name" in item:
                user_item["given_name"] = item["given_name"]
            if "family_name" in item:
                user_item["family_name"] = item["family_name"]
            if "phone_number" in item:
                user_item["phone_number"] = item["phone_number"]
            
            # Create the user record
            table.put_item(Item=user_item)
            print(f"✅ Created admin user record with sub: {cognito_sub}")
            print(f"Item: {json.dumps(user_item, indent=2)}")
            return
            
        # Update existing user record
        item = response['Item']
        item['sub'] = cognito_sub
        
        # Update the user record
        table.put_item(Item=item)
        print(f"✅ Updated admin user record with sub: {cognito_sub}")
        print(f"Item: {json.dumps(item, indent=2)}")
        
    except Exception as e:
        print(f"❌ Error updating admin user: {e}")

if __name__ == "__main__":
    print(f"Updating admin user record (ID: {ADMIN_USER_ID})...")
    sub = get_admin_cognito_sub()
    update_admin_user_with_sub(sub)
