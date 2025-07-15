# DynamoDB Reference for Matt's Cognito SSO Project

## Single-Table Design Pattern

This document provides a detailed example of how to structure data in DynamoDB for the SSO system, aligned with Sir Jamby's reference but using a coffee app context for clarity.

## Main Table Design (matt-cognito-hop-main)

### Application Entity
```json
{
    "PK": "application-mattcoffee",
    "SK": "application",
    "application_id": "mattcoffee",
    "name": "Matt's Coffee Rewards",
    "channels": [
        {
            "channel_id": "mobile",
            "return_url": "mattscoffee://auth/callback"
        },
        {
            "channel_id": "web",
            "return_url": "https://rewards.mattscoffee.com/auth/callback"
        },
        {
            "channel_id": "kiosk",
            "return_url": "https://kiosk.mattscoffee.com/auth/success"
        }
    ],
    "created_at": "2025-07-01T10:00:00Z"
}
```

### User Entity
```json
{
    "PK": "user-u123456",
    "SK": "user",
    "user_id": "u123456",
    "sub": "a1b2c3d4-e5f6-g7h8-i9j0-k1l2m3n4o5p6",
    "email": "coffee.lover@example.com",
    "name": "Coffee Lover",
    "phone_number": "+1234567890",
    "gender": "female",
    "accepts_marketing": "true",
    "created_at": "2025-07-10T14:30:00Z"
}
```

### Application-User Entity (Authorization)
```json
{
    "PK": "application-mattcoffee",
    "SK": "user-u123456",
    "application_id": "mattcoffee",
    "user_id": "u123456",
    "roles": ["customer", "rewards_member"],
    "created_at": "2025-07-10T14:35:00Z"
}
```

### Session Entity
```json
{
    "PK": "user-u123456",
    "SK": "session-s789abc",
    "session_id": "s789abc",
    "user_id": "u123456",
    "tokenset": {
        "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
        "id_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
        "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
    },
    "expires_at": "2025-07-16T14:00:00Z",
    "created_at": "2025-07-15T14:00:00Z"
}
```

## Orders Table (matt-cognito-hop-orders)

```json
{
    "PK": "user-u123456",
    "SK": "order-o987654",
    "user_id": "u123456",
    "order_id": "o987654",
    "order_details": {
        "amount": 15.47,
        "items": [
            {
                "item_id": "latte-lg",
                "name": "Large Vanilla Latte",
                "quantity": 1,
                "price": 5.99
            },
            {
                "item_id": "muffin-blueberry",
                "name": "Blueberry Muffin",
                "quantity": 2,
                "price": 3.99
            },
            {
                "item_id": "water-sm",
                "name": "Small Bottled Water",
                "quantity": 1,
                "price": 1.50
            }
        ],
        "store_id": "store-downtown",
        "store_name": "Matt's Coffee - Downtown"
    },
    "status": "completed",
    "created_at": "2025-07-14T09:15:00Z"
}
```

## Common Access Patterns

### 1. Validate Application and Channel
```
Query:
- PK = "application-mattcoffee"
- SK = "application"

Then check if channel_id exists in the channels array
```

### 2. Check if User is Authorized for Application
```
Query:
- PK = "application-mattcoffee"
- SK = "user-u123456"

If record exists, user is authorized
```

### 3. Get User Details
```
Query:
- PK = "user-u123456"
- SK = "user"
```

### 4. Create/Retrieve Session
```
Create:
- PK = "user-u123456"
- SK = "session-{new_session_id}"

Retrieve:
- PK = "user-u123456"
- SK = "session-s789abc"
```

### 5. Get User Orders
```
Query (on Orders table):
- PK = "user-u123456"
- SK begins_with "order-"
```

## SSO Flow with DynamoDB

1. **User visits Matt's Coffee Mobile App**:
   - App redirects to SSO with `application_id=mattcoffee&channel_id=mobile`

2. **SSO Backend validates the application and channel**:
   - Queries DynamoDB: `PK="application-mattcoffee", SK="application"`
   - Checks if the channel "mobile" exists in the channels array

3. **User logs in via SSO**:
   - Cognito authenticates the user and returns tokens

4. **SSO Backend checks if user is authorized for this app**:
   - Queries DynamoDB: `PK="application-mattcoffee", SK="user-u123456"`
   - If record exists, user is authorized

5. **SSO Backend creates a session**:
   - Creates record: `PK="user-u123456", SK="session-s789abc"`
   - Stores the token set from Cognito
   - Returns session_id to the SSO Frontend

6. **SSO Frontend redirects back to the app**:
   - Redirects to: `mattscoffee://auth/callback?session_id=s789abc`

7. **App retrieves the tokens**:
   - App calls SSO Backend with session_id
   - SSO Backend returns the token set
   - App can now use these tokens to call the Matt's Coffee API

8. **App shows orders**:
   - App calls Matt's Coffee API with the access token
   - API validates the token and identifies the user
   - API queries Orders table: `PK="user-u123456", SK begins_with "order-"`
   - Returns the user's coffee orders
