# Onboarding Challenge Cognito

A serverless application implementing Single Sign-On (SSO) with AWS Cognito and DynamoDB.

## Architecture

### Backend 
- **SSO Backend**: Handles authentication, user management, and session control (4 APIs deployed)
- **Client Backend**: Manages application-specific features (e.g., orders) (1 API deployed)

### Frontend 🔄 NEXT PHASE
- **SSO Frontend**: User authentication interface
- **Client Application**: Business application using SSO

## Project Structure

```
/cognito-hop/
├── backend/
│   ├── sso_backend/         # SSO backend services
│   │   ├── app/
│   │   │   ├── domains/     # Business logic
│   │   │   ├── handlers/    # Lambda handlers
│   │   │   ├── services/    # External integrations
│   │   │   └── utils/       # Utility functions
│   │   ├── serverless.yml   # Serverless config
│   │   └── .env.*.yml       # Environment variables
│   └── client_backend/      # Client application backend
└── frontend/
    ├── sso_frontend/        # SSO interface
    └── client_frontend/     # Client application UI
```

## AWS Resources
- Cognito User Pool
- DynamoDB Tables (main + orders)
- Lambda Functions
- API Gateway
