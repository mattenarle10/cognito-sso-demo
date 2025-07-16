// cognito configuration
export const COGNITO_CONFIG = {
  userPoolId: import.meta.env.VITE_COGNITO_USER_POOL_ID,
  userPoolClientId: import.meta.env.VITE_COGNITO_CLIENT_ID,
  region: import.meta.env.VITE_AWS_REGION
}

// sso backend api endpoints (this frontend only calls SSO backend)
export const API_CONFIG = {
  ssoBaseUrl: import.meta.env.VITE_SSO_API_URL,
  endpoints: {
    validateAppChannel: '/validate-app-channel',
    checkAppUser: '/check-app-user', 
    initSession: '/init-session',
    getSession: '/get-session'
  }
}


// route names
export const ROUTES = {
  LOGIN: 'login',
  REGISTER: 'register'
} as const 