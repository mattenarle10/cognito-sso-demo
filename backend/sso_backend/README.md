# SSO Backend

This is the SSO backend for the Cognito SSO project. It handles user authentication, session management, and application authorization.

## Architecture

The SSO backend follows a clean, modular architecture with the following components:

- **Handlers**: Lambda function entry points
  - **Triggers**: Cognito triggers (e.g., post-confirmation)
  - **HTTP**: API Gateway endpoints
- **Domains**: Business logic
- **Services**: External service integrations
  - **AWS**: AWS service wrappers
  - **Repositories**: Data access layer
- **Utils**: Utility functions

## Environment Setup

1. Create a `.env.dev.yml` file with the following environment variables:
   ```yaml
   MAIN_TABLE: matt-cognito-hop-main
   COGNITO_USER_POOL_ID: ap-southeast-2_VwKhOLJk1
   COGNITO_APP_CLIENT_ID: 7gl0eh7v9ftv5j0pvs6rt92mo6
   AWS_NODEJS_CONNECTION_REUSE_ENABLED: 1
   ```

## Deployment

### Prerequisites
- Node.js and npm installed
- Serverless Framework v4 installed: `npm install -g serverless`
- AWS CLI configured with appropriate credentials

### Deploy to AWS
```bash
# Install Python dependencies
pip install -r requirements.txt

# Install Serverless plugins
npm install

# Deploy to dev environment
serverless deploy --stage dev
```

## Post-Confirmation Lambda

The post-confirmation Lambda function is triggered after a user confirms their registration in Cognito. It performs the following actions:

1. Extracts user attributes from the Cognito event
2. Creates a user record in DynamoDB
3. Creates an application-user relationship record in DynamoDB

### Testing the Post-Confirmation Lambda

1. Deploy the SSO backend using the instructions above
2. Configure the Lambda as a post-confirmation trigger in your Cognito User Pool:
   - Go to the AWS Console > Cognito > User Pools > Your User Pool
   - Under "User Pool Properties" > "Lambda Triggers"
   - Set the "Post confirmation" trigger to your deployed Lambda function
3. Register a new user in Cognito
4. Confirm the user with the verification code
5. Check CloudWatch logs to verify the Lambda execution
6. Check DynamoDB to verify that the user and application-user records were created

## Next Steps

After successfully testing the post-confirmation Lambda, the next steps are:

1. Implement the SSO Backend APIs:
   - `GET /validate-app-channel`
   - `GET /check-app-user`
   - `POST /init-session`
   - `GET /get-session`
2. Implement JWT validation helper
3. Implement the client backend
