# Cognito SSO Implementation Plan

## Current Progress

### Phase 1: Cognito Setup (Completed) ✅
- Created Cognito User Pool with email as username
- Added required attributes: name, email, phone number
- Added custom attributes: gender, accepts_marketing
- Created App Client with USER_PASSWORD_AUTH flow
- Noted down User Pool ID, App Client ID, and Region

### Phase 2: DynamoDB Setup (Completed) ✅
- Created main table: matt-cognito-hop-main
- Created orders table: matt-cognito-hop-orders
- Added sample application record with channels and return URLs

## Current Phase: Phase 3 - SSO Backend

### Step 1: Post-Confirmation Lambda (In Progress) 🔄
- [x] Created directory structure for SSO backend
- [x] Implemented post_confirmation.py Lambda handler
- [x] Updated serverless.yml to include the post-confirmation trigger
- [ ] Deploy and attach Lambda to Cognito User Pool
- [ ] Test with a new user registration

### Step 2: SSO Backend APIs (Next) 🔜
1. `GET /validate-app-channel` → checks if application_id + channel_id exist
2. `GET /check-app-user` → checks if user is authorized for the app
3. `POST /init-session` → stores token set, returns session_id
4. `GET /get-session` → given session_id, return token set

### Step 3: JWT Helper (Future) 📅
- Implement JWT validation using Cognito JWKS

## Future Phases

### Phase 4: Client Backend
- `GET /orders` → Validate ID Token and return user's orders

### Phase 5: Frontend Applications
- Implement SSO Frontend (Login, Register)
- Implement Client Frontend (Home, Orders)

## Next Actions

1. **Deploy Post-Confirmation Lambda**
   - Run `serverless deploy` for the SSO backend
   - Attach the Lambda to Cognito User Pool as a Post Confirmation trigger

2. **Test Post-Confirmation Lambda**
   - Register a new user in Cognito
   - Confirm the user with OTP
   - Verify that the Lambda function is triggered (check CloudWatch logs)
   - Verify that the user record is created in DynamoDB
   - Verify that the application-user relationship record is created in DynamoDB

3. **Implement SSO Backend APIs one by one**
   - Start with `validate-app-channel` API
   - Follow with the other APIs in sequence
   - Test each API thoroughly before moving to the next
