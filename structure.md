# Cognito SSO Project Structure

## Project Overview

This project implements a serverless architecture for a Cognito-based Single Sign-On (SSO) system with the following components:

```
/cognito-hop/
├── backend/
│   ├── sso_backend/              # SSO Backend
│   │   ├── serverless.yml        # Serverless config for SSO backend
│   │   ├── app/
│   │   │   ├── domains/          # Business logic
│   │   │   │   ├── user_domain.py
│   │   │   │   ├── application_domain.py
│   │   │   │   └── session_domain.py
│   │   │   ├── handlers/         # Lambda handlers
│   │   │   │   ├── triggers/     # Cognito triggers
│   │   │   │   │   └── post_confirmation.py
│   │   │   │   └── http/         # API endpoints
│   │   │   │       ├── validate_app_channel.py
│   │   │   │       ├── check_app_user.py
│   │   │   │       ├── init_session.py
│   │   │   │       └── get_session.py
│   │   │   ├── services/         # External service integrations
│   │   │   │   ├── aws/          # AWS service wrappers
│   │   │   │   │   ├── cognito_service.py
│   │   │   │   │   └── dynamodb_service.py
│   │   │   │   └── repositories/ # Database access
│   │   │   │       ├── user_repository.py
│   │   │   │       ├── application_repository.py
│   │   │   │       └── session_repository.py
│   │   │   └── utils/            # Utility functions
│   │   │       ├── response.py   # API response formatting
│   │   │       ├── jwt_helper.py # JWT validation
│   │   │       └── exceptions.py # Custom exceptions
│   │   └── requirements.txt      # Python dependencies for SSO backend
│   └── client_backend/           # Client Backend
│       ├── serverless.yml        # Serverless config for client backend
│       ├── app/
│       │   ├── domains/          # Business logic
│       │   │   └── order_domain.py
│       │   ├── handlers/         # Lambda handlers
│       │   │   └── http/         # API endpoints
│       │   │       └── get_orders.py
│       │   ├── services/         # External service integrations
│       │   │   ├── aws/          # AWS service wrappers
│       │   │   │   └── dynamodb_service.py
│       │   │   └── repositories/ # Database access
│       │   │       └── order_repository.py
│       │   └── utils/            # Utility functions
│       │       ├── response.py   # API response formatting
│       │       └── jwt_helper.py # JWT validation
│       └── requirements.txt      # Python dependencies for client backend
├── frontend/
│   ├── sso_fe/                   # Vue app for SSO
│   │   └── src/                  # SSO frontend source code
│   └── client_fe/                # Vue app for client app
│       └── src/                  # Client frontend source code
└── README.md
```

## Implementation Plan

### Phase 1: Cognito Setup (Completed)
- Created Cognito User Pool with email as username
- Added required attributes: name, email, phone number
- Added custom attributes: gender, accepts_marketing
- Created App Client with USER_PASSWORD_AUTH flow

### Phase 2: DynamoDB Setup (Completed)
- Created main table: matt-cognito-hop-main
- Created orders table: matt-cognito-hop-orders
- Added sample application record

### Phase 3: SSO Backend (Current Phase)

#### Step 1: Post-Confirmation Lambda
- Implement Lambda function triggered after user confirmation
- Save user data to DynamoDB
- Create application-user relationship

#### Step 2: SSO Backend APIs
- `GET /validate-app-channel` → checks if application_id + channel_id exist
- `GET /check-app-user` → checks if user is authorized for the app
- `POST /init-session` → stores token set, returns session_id
- `GET /get-session` → given session_id, return token set

#### Step 3: JWT Helper
- Implement JWT validation using Cognito JWKS

### Phase 4: Client Backend
- `GET /orders` → Validate ID Token and return user's orders

### Phase 5: Frontend Applications
- Implement SSO Frontend (Login, Register)
- Implement Client Frontend (Home, Orders)


### 🔧 Step-by-step Cognito Setup 

1. **Create a User Pool**
    - Enable email as username
    - Enable phone number as an attribute (but not required)
    - Turn on email OTP (confirmation required)
    - Enable password auth flow
2. **Create an App Client**
    - Disable client secret (for frontends)
    - Enable Cognito User Pool token grant
    - Enable refresh token expiration
3. **Configure Lambda Triggers**
    - **PostConfirmation** trigger → write user info to DynamoDB
    - (Optional) **PreSignUp** for extra validation
4. **Get Cognito Pool + Client IDs**
    - Needed for Vue + BE token validation

---


## ⚙️ Phase 2: DynamoDB Setup

Design this early for smooth dev. You’ll use a **single-table design** with smart PK/SK patterns:

### DynamoDB Schema (Single-Table Design)

#### Applications Entity
```json
{
    "PK": "application-{id}",
    "SK": "application",
    "application_id": "{id}",
    "channels": [
        {
            "channel_id": "{channel_id}",
            "return_url": "{return_url}"
        }
    ],
    "created_at": "{timestamp}"
}
```

#### Application-User Entity
```json
{
    "PK": "application-{id}",
    "SK": "user-{user_id}",
    "application_id": "{id}",
    "user_id": "{user_id}",
    "created_at": "{timestamp}"
}
```

#### User Entity
```json
{
    "PK": "user-{user_id}",
    "SK": "user",
    "sub": "{cognito_sub}",
    "email": "{email}",
    "phone": "{phone}",
    "name": "{name}",
    "gender": "{gender}",
    "accepts_marketing": "{boolean}",
    "created_at": "{timestamp}"
}
```

#### Session Entity
```json
{
    "PK": "user-{user_id}",
    "SK": "session-{session_id}",
    "session_id": "{session_id}",
    "token_set": {
        "id_token": "{id_token}",
        "access_token": "{access_token}",
        "refresh_token": "{refresh_token}"
    },
    "expires_at": "{timestamp}",
    "created_at": "{timestamp}"
}
```

**Separate Table: Orders**
```json
{
    "PK": "user-{user_id}",
    "SK": "order-{order_id}",
    "order_id": "{order_id}",
    "order_details": {
        "amount": "{amount}",
        "items": [
            {
                "item_id": "{item_id}",
                "quantity": "{quantity}",
                "price": "{price}"
            }
        ]
    },
    "status": "{status}",
    "created_at": "{timestamp}"
}
```

Set this up with `boto3` scripts or AWS Console.

---

## 🧱 Phase 3: Backend (SSO BE First)

Start backend now that Cognito + DB are clear.

### 🔐 SSO Backend Responsibilities

- `/authorize` → Validates app/channel
- `/check-app-user` → Is this user authorized for this app?
- `/init-session` → Stores tokenset, returns `session_id`
- `/get-session` → Gets tokenset via `session_id`
- 🔁 **PostConfirmation Lambda**:
    - Create User
    - Create App-User

Use `python-jose` for JWT validation and `boto3` for Cognito/DynamoDB interaction.

Structure in OOP:

- `services/auth_service.py`
- `models/session.py`, `models/user.py`
- `routes/sso_routes.py`

---

## 🧱 Phase 4: Backend (Client BE)

Responsibilities:

- `/orders` GET
    - Extract and verify ID token
    - Decode `sub`
    - Query DynamoDB for orders
    - Return data

Use same JWT verifier (`python-jose`) + OOP patterns.

---

## 🎨 Phase 5: Frontends (Vue.js)

### 🖥️ SSO FE (Vue)

- Login
    - Cognito Login (JS SDK or API call)
    - Redirect to SSO BE for session creation
    - Redirect to client FE with `session_id`
- Register
    - Register via Cognito SDK
    - Enter OTP → confirm email
    - Redirect flow as above

### 🛍️ Client FE (Vue)

- `/` → Logged out homepage
- `/success?session_id=...`
    - Get token set via SSO BE `/get-session`
    - Store tokenset locally
- `/orders`
    - Authenticated page → shows user orders

---

## 🧪 Phase 6: End-to-End Flow Testing

1. Register from client → SSO FE
2. OTP flow, user created in Cognito + DynamoDB
3. App-user record created
4. Session created + passed via URL
5. Orders queried by BE with JWT verification

---