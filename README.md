# Cognito SSO Challenge - Single Sign-On Implementation

A serverless application implementing Single Sign-On (SSO) with AWS Cognito, DynamoDB, and Vue.js frontends. This project demonstrates a complete authentication flow between separate applications.

## Architecture Overview

### Backend Services
- **SSO Backend**: Authentication service handling sessions and token management
  - REST APIs via API Gateway and Lambda
  - Cognito integration with custom triggers
  - DynamoDB for data storage
  - Profile management with Cognito+DynamoDB sync
  - OAuth-style authorization system
  
- **Client Backend**: Business application backend
  - Protected APIs requiring token authentication
  - Orders management

### Frontend Applications
- **SSO Frontend** ✅ COMPLETED
  - Vue.js application for authentication
  - Login and registration with verification
  - Security consent screens
  - Account management with profile editing
  - Authorization management interface
  
- **Client Application** ✅ COMPLETED
  - Vue.js business application
  - Authentication integration
  - Protected content (orders)
  - Profile management integration

- **Admin Portal** 🚧 PLANNED
  - Vue 3 + Vite application for administrators
  - User management interface
  - User deactivation and deletion
  - Force password reset functionality
  - User profile editing capabilities

## Authentication Flow

1. User clicks "Login" on Client App → redirected to SSO Frontend
2. User authenticates via SSO Frontend with Cognito
3. SSO Backend creates a secure session
4. User redirected back to Client App 
5. Client App securely exchanges credentials
6. User accesses protected resources

## Project Structure

```
/cognito-hop/
├── backend/
│   ├── sso_backend/         # SSO backend services
│   |── admin_backend/       # Admin-specific APIs
│   └── client_backend/      # Client application backend
└── frontend/
    ├── sso_frontend/        # SSO interface (Vue.js)
    ├── admin_portal/        # Admin portal (Vue 3 + Vite)
    └── client_app/          # Client application UI (Vue.js)
```

## AWS Resources

- **Cognito User Pool** - Authentication management
- **DynamoDB Tables** - Data storage
- **Lambda Functions** - Serverless computing
- **API Gateway** - API management

## Setup Instructions

### Prerequisites

- Node.js
- Python
- AWS CLI configured
- Serverless Framework

### Backend Setup

```bash
# SSO Backend
cd backend/sso_backend
npm install
sls deploy

# Client Backend
cd backend/client_backend
npm install
sls deploy
```

### Frontend Setup

```bash
# SSO Frontend
cd frontend/sso_frontend
npm install
npm run dev

# Client Frontend
cd frontend/client_app
npm install
npm run dev
```
