## Master Checklist (Grouped by Scope)

---
client id: 7gl0eh7v9ftv5j0pvs6rt92mo6

### 🏗️ **PHASE 0: Architecture & Planning**

- [x]  Define SSO flow and responsibilities (SSO vs Client)
- [x]  Decide domain/subdomain structure (e.g. `sso.smadvantage.com`, `smac.ph`)
- [x]  Choose technology: Cognito + Vue.js + Python (OOP) + DynamoDB
- [x]  Plan single-table DynamoDB design (See `dynamo_reference.md` for detailed schema)
- [x]  Plan separation of SSO vs Client apps and teams

---

### 🔐 **PHASE 1: Cognito Setup (ClickOps First)**

- [x]  Create Cognito User Pool
    - [x]  Enable username as email
    - [x]  Require email and password on signup
    - [x]  Enable email OTP confirmation
- [x]  Create App Client (no client secret)
    - [x]  Allow "USER_PASSWORD_AUTH"
    - [x]  Enable token expiration
- [ ]  Enable Lambda triggers
    - [ ]  **PostConfirmation** trigger to save user to DynamoDB (in progress)
- [x]  Note down:
    - [x]  User Pool ID: ap-southeast-2_VwKhOLJk1
    - [x]  App Client ID: 7gl0eh7v9ftv5j0pvs6rt92mo6
    - [x]  Region: ap-southeast-2

---

### 🗄️ **PHASE 2: DynamoDB Setup**

- [x]  Create **Main Table**
    - [x]  `application`
    - [x]  `user`
    - [x]  `application-user`
    - [x]  `session`
- [x]  Create **Orders Table**
    - [x]  With `user_id`, `order_id`
- [x]  Write sample seed data:
    - [x]  Sample application + channel + return URL

---

### ⚙️ **PHASE 3: SSO Backend (Python OOP)**

- [ ]  API: `GET /validate-app-channel` → checks if `application_id` + `channel_id` exist
- [ ]  API: `GET /check-app-user` → checks if user is authorized for the app
- [ ]  API: `POST /init-session` → stores token set, returns session_id
- [ ]  API: `GET /get-session` → given session_id, return token set
- [x]  Lambda: `post_confirmation.py` → saves user + app-user in DynamoDB (implementation complete, pending deployment)
- [ ]  JWT Helper: Validate Cognito ID tokens using Cognito JWKS
- [ ]  DynamoDB Helper: Store + read from single-table design
- [ ]  Error Handling: 403 if app not authorized

---

### ⚙️ **PHASE 4: Client Backend (Python OOP)**

- [ ]  API: `GET /orders`
    - [ ]  Validate ID Token from header
    - [ ]  Extract `sub` as `user_id`
    - [ ]  Query orders table for user
    - [ ]  Return list of orders

---

### 🎨 **PHASE 5: SSO Frontend (Vue.js)**

- [ ]  Page: `/login`
    - [ ]  Form for email + password
    - [ ]  Redirect from client includes `application_name` and `channel_id`
    - [ ]  Validate app/channel via SSO BE
    - [ ]  Login via Cognito
    - [ ]  Call SSO BE to check user auth
    - [ ]  Call SSO BE to initialize session
    - [ ]  Redirect to client app with `session_id`
- [ ]  Page: `/register`
    - [ ]  Form for email, phone, name, gender, password
    - [ ]  Register via Cognito
    - [ ]  OTP verification screen
    - [ ]  After confirmation, call same flow as login

---

### 🎨 **PHASE 6: Client Frontend (Vue.js)**

- [ ]  Page: `/` homepage (not logged in)
- [ ]  Page: `/success?session_id=xxx`
    - [ ]  Call SSO BE to fetch token set
    - [ ]  Store tokenset locally
    - [ ]  Redirect to `/orders`
- [ ]  Page: `/orders`
    - [ ]  Fetch orders using ID token in header
    - [ ]  Display orders for user
- [ ]  (Optional) Page: `create-order` form

---

### 🔁 **PHASE 7: End-to-End Flow Testing**

- [ ]  Register a user
- [ ]  Confirm email via OTP
- [ ]  Ensure user is created in DynamoDB with app-user link
- [ ]  Login works with token set returned
- [ ]  Session is created in DynamoDB
- [ ]  Redirect to client with `session_id`
- [ ]  Fetch tokenset using `session_id`
- [ ]  Access orders using verified JWT

---

### 🛡️ **PHASE 8: Security, Cleanups, and Docs**

- [ ]  Secure all endpoints with token validation
- [ ]  Use short-lived tokens + refresh if needed
- [ ]  Hide secrets in `.env`
- [ ]  Add README.md with flow diagram + instructions
- [ ]  Add logs for session creation and errors