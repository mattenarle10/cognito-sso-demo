#!/usr/bin/env python3
"""
script to add test orders for our existing user
run this to populate orders table for testing
"""

import boto3
import uuid
from datetime import datetime, timedelta
import json
from decimal import Decimal

# dynamodb setup
dynamodb = boto3.resource('dynamodb', region_name='ap-southeast-2')
orders_table = dynamodb.Table('matt-cognito-hop-orders')

# our existing user (from post confirmation)
USER_ID = "user-9fef7f58"  # the user we created when registering mattenarle10@gmail.com

def create_test_orders():
    """create sample orders for testing"""
    
    test_orders = [
        {
            "PK": USER_ID,
            "SK": f"order-{str(uuid.uuid4())[:8]}",
            "order_id": f"order-{str(uuid.uuid4())[:8]}",
            "user_id": USER_ID,
            "order_details": {
                "items": [
                    {"name": "cappuccino", "quantity": 2, "price": Decimal('4.50')},
                    {"name": "croissant", "quantity": 1, "price": Decimal('3.25')}
                ],
                "total_amount": Decimal('12.25'),
                "currency": "AUD"
            },
            "status": "completed",
            "created_at": (datetime.now() - timedelta(days=2)).isoformat(),
            "completed_at": (datetime.now() - timedelta(days=2, hours=-1)).isoformat()
        },
        {
            "PK": USER_ID,
            "SK": f"order-{str(uuid.uuid4())[:8]}",
            "order_id": f"order-{str(uuid.uuid4())[:8]}",
            "user_id": USER_ID,
            "order_details": {
                "items": [
                    {"name": "flat white", "quantity": 1, "price": Decimal('4.00')},
                    {"name": "blueberry muffin", "quantity": 1, "price": Decimal('4.50')}
                ],
                "total_amount": Decimal('8.50'),
                "currency": "AUD"
            },
            "status": "completed",
            "created_at": (datetime.now() - timedelta(days=1)).isoformat(),
            "completed_at": (datetime.now() - timedelta(days=1, hours=-0.5)).isoformat()
        },
        {
            "PK": USER_ID,
            "SK": f"order-{str(uuid.uuid4())[:8]}",
            "order_id": f"order-{str(uuid.uuid4())[:8]}",
            "user_id": USER_ID,
            "order_details": {
                "items": [
                    {"name": "latte", "quantity": 1, "price": Decimal('4.25')},
                    {"name": "avocado toast", "quantity": 1, "price": Decimal('12.00')}
                ],
                "total_amount": Decimal('16.25'),
                "currency": "AUD"
            },
            "status": "preparing",
            "created_at": datetime.now().isoformat()
        }
    ]
    
    print(f"adding {len(test_orders)} test orders for user {USER_ID}...")
    
    for order in test_orders:
        try:
            orders_table.put_item(Item=order)
            print(f"✅ added order {order['order_id']}")
        except Exception as e:
            print(f"❌ failed to add order {order['order_id']}: {str(e)}")
    
    print(f"\n🎉 test orders created successfully!")
    print(f"user {USER_ID} now has {len(test_orders)} orders")

if __name__ == "__main__":
    create_test_orders() 