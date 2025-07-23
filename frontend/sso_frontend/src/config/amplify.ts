import { Amplify } from 'aws-amplify';
import { cognitoUserPoolsTokenProvider } from 'aws-amplify/auth/cognito';

// Initialize Amplify with your Cognito configuration
export const configureAmplify = () => {
  // Log environment variables for debugging (will be removed in production)
  console.log('Amplify Configuration:', {
    region: import.meta.env.VITE_COGNITO_REGION,
    userPoolId: import.meta.env.VITE_COGNITO_USER_POOL_ID,
    clientId: import.meta.env.VITE_COGNITO_CLIENT_ID,
    domain: import.meta.env.VITE_COGNITO_DOMAIN
  });

  // Clean the domain - remove any protocol prefix
  const cognitoDomain = (import.meta.env.VITE_COGNITO_DOMAIN || '').replace(/^https?:\/\//, '');
  
  // Configure Amplify with the v6 structure
  Amplify.configure({
    Auth: {
      Cognito: {
        userPoolId: import.meta.env.VITE_COGNITO_USER_POOL_ID || '',
        userPoolClientId: import.meta.env.VITE_COGNITO_CLIENT_ID || '',
        loginWith: {
          oauth: {
            domain: cognitoDomain,
            scopes: ['email', 'profile', 'openid', 'phone'],
            redirectSignIn: [`${window.location.origin}/auth/callback`],
            redirectSignOut: [`${window.location.origin}/`],
            responseType: 'code'
          }
        }
      }
    }
  });
  
  // Configure token storage
  cognitoUserPoolsTokenProvider.setKeyValueStorage({
    getItem(key: string) {
      return Promise.resolve(localStorage.getItem(key));
    },
    setItem(key: string, value: string) {
      localStorage.setItem(key, value);
      return Promise.resolve();
    },
    removeItem(key: string) {
      localStorage.removeItem(key);
      return Promise.resolve();
    },
    clear() {
      localStorage.clear();
      return Promise.resolve();
    }
  });
  
  console.log('Amplify configured successfully');
};

export default configureAmplify;
