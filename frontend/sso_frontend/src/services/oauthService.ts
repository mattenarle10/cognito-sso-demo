import { signInWithRedirect, fetchUserAttributes, fetchAuthSession, signOut, updateUserAttributes as amplifyUpdateUserAttributes } from 'aws-amplify/auth';
import { getCurrentUser } from 'aws-amplify/auth';

// Define our own token interface that matches what we need in the app and Amplify v6 tokens
export interface AuthTokens {
  accessToken: string;
  idToken: string;
  refreshToken: string; // Required for token refresh operations
}

// Define types for user attributes compatible with Amplify v6
export type UserAttributes = {
  [key: string]: string;
};

// Auth Service class for handling authentication operations
export class AuthService {
  /**
   * Sign in with Google using Amplify's federated sign-in
   */
  async signInWithGoogle(): Promise<void> {
    try {
      // For SSO flow, always sign out first to ensure fresh authentication
      // This forces Google account selection by clearing all sessions
      try {
        await signOut();
        console.log('Cleared Amplify sessions');
        
        // Also clear browser storage to force fresh Google OAuth
        localStorage.clear();
        sessionStorage.clear();
        
        // Clear specific Amplify OAuth storage
        localStorage.removeItem('amplify-signin-with-hostedUI');
        localStorage.removeItem('amplify-oauth-state');
        
        // Clear any Cognito session cookies
        document.cookie.split(";").forEach(function(c) { 
          document.cookie = c.replace(/^ +/, "").replace(/=.*/, "=;expires=" + new Date().toUTCString() + ";path=/"); 
        });
        
        console.log('Cleared all browser storage and cookies for fresh OAuth');
      } catch (e) {
        console.log('No existing session to clear');
      }
      
      // Get OAuth parameters from sessionStorage to include in state
      const appName = sessionStorage.getItem('oauth_application_name')
      const channelId = sessionStorage.getItem('oauth_channel_id')
      const redirectUrl = sessionStorage.getItem('oauth_redirect_url')
      
      // Create custom state with parameters
      const customState = {
        application_name: appName,
        channel_id: channelId,
        redirect_url: redirectUrl
      }
      
      await signInWithRedirect({ 
        provider: 'Google',
        customState: JSON.stringify(customState)
      });
    } catch (err: any) {
      if (err.name === 'UserAlreadyAuthenticatedException') {
        console.log('User already authenticated - handling SSO flow');
        // This is expected in SSO flow - redirect to appropriate page
        return;
      }
      console.error('Error signing in with Google:', err);
      throw err;
    }
  }

  /**
   * Get the current authenticated user
   */
  async getCurrentUser() {
    try {
      // Check if we have valid tokens first
      const session = await this.getCurrentSession();
      if (!session) {
        return null;
      }
      
      return await getCurrentUser();
    } catch (err: any) {
      // Not authenticated - this is expected behavior
      console.log('No authenticated user found');
      return null;
    }
  }

  /**
   * Get current session including tokens
   * Enhanced with OAuth timing handling for Google OAuth flow
   */
  async getCurrentSession(): Promise<AuthTokens | null> {
    try {
      const session = await fetchAuthSession();
      
      // Check if tokens exist in the session
      if (!session.tokens) {
        console.log('Session tokens not yet available');
        return null;
      }
      
      // Safely access token properties with proper type handling
      const idToken = session.tokens.idToken?.toString();
      const accessToken = session.tokens.accessToken?.toString();
      
      // For OAuth flows, refreshToken might not be immediately available
      // Handle different token structures in Amplify v6
      let refreshToken = '';
      if ('refreshToken' in session.tokens && session.tokens.refreshToken) {
        refreshToken = session.tokens.refreshToken.toString();
      }
      
      if (!idToken || !accessToken) {
        console.log('Required tokens (idToken, accessToken) not yet available');
        return null;
      }
      
      // Tokens retrieved successfully
      
      // Return tokens in the format expected by our AuthTokens interface
      return {
        idToken,
        accessToken,
        refreshToken
      };
    } catch (err: any) {
      console.log('Session not ready yet');
      return null;
    }
  }

  /**
   * Wait for OAuth tokens with exponential backoff
   * Specifically for Google OAuth flow timing issues
   */
  async waitForOAuthTokens(maxAttempts: number = 10): Promise<AuthTokens | null> {
    let attempts = 0;
    
    while (attempts < maxAttempts) {
      const tokens = await this.getCurrentSession();
      if (tokens) {
        // OAuth tokens retrieved successfully
        return tokens;
      }
      
      attempts++;
      const waitTime = Math.min(500 * Math.pow(2, attempts), 5000); // Exponential backoff, max 5s
      // Waiting for OAuth tokens with exponential backoff
      await new Promise(resolve => setTimeout(resolve, waitTime));
    }
    
    console.error('Failed to retrieve OAuth tokens after maximum attempts');
    return null;
  }

  /**
   * Update user attributes
   */
  async updateUserAttributes(attributes: UserAttributes): Promise<boolean> {
    try {
      await amplifyUpdateUserAttributes({
        userAttributes: attributes
      });
      return true;
    } catch (err: any) {
      console.error('Error updating user attributes:', err);
      return false;
    }
  }

  /**
   * Sign out the user
   */
  async signOut(): Promise<void> {
    try {
      await signOut();
    } catch (err: any) {
      console.error('Error signing out:', err);
      throw err;
    }
  }

  /**
   * Check if user needs to complete their profile
   * This is determined by checking if phone_number is missing or has placeholder value
   */
  async checkNeedsProfileCompletion(): Promise<boolean> {
    try {
      // First check if we can get a user at all
      const user = await this.getCurrentUser();
      if (!user) return false;
      
      // In Amplify v6, we need to fetch attributes separately
      const attributes = await fetchUserAttributes();
      
      // Check if phone_number is missing or has placeholder value
      return !attributes['phone_number'] || attributes['phone_number'] === '+00000000000';
    } catch (error: any) {
      console.error('Error checking profile completion status:', error);
      return false;
    }
  }

  /**
   * Complete Google OAuth flow with SSO backend integration
   * Uses existing APIs from useApi composable
   */
  async processGoogleOAuth(applicationName: string, channelId: string, redirectUrl?: string) {
    // Import useApi dynamically to avoid circular dependencies
    const { useApi } = await import('@/composables/useApi');
    const api = useApi();

    try {
      // Step 1: Validate application and channel using existing API
      const appValidation = await api.validateAppChannel(applicationName, channelId);
      if (!appValidation?.valid) {
        throw new Error('Invalid application or channel');
      }

      // Step 2: Wait for OAuth tokens with proper timing
      const tokens = await this.waitForOAuthTokens();
      if (!tokens) {
        throw new Error('Failed to retrieve OAuth tokens - please try signing in again');
      }

      // Step 3: Get raw session to extract proper JWT tokens for backend validation
      const rawSession = await fetchAuthSession();
      
      // Format tokens for backend - backend expects raw JWT tokens
      const backendTokens = {
        id_token: rawSession.tokens?.idToken?.toString(),
        access_token: rawSession.tokens?.accessToken?.toString(),
        refresh_token: (rawSession.tokens && 'refreshToken' in rawSession.tokens && rawSession.tokens.refreshToken) ? rawSession.tokens.refreshToken.toString() : '',
        token_type: 'Bearer',
        expires_in: rawSession.tokens?.accessToken?.payload?.exp || 3600
      };
      
      // Tokens extracted for backend validation
      
      // Validate we have the required tokens
      if (!backendTokens.id_token || !backendTokens.access_token) {
        throw new Error('Missing required tokens for backend validation');
      }

      // Step 4: Check if profile completion is needed FIRST
      const needsProfileCompletion = await this.checkNeedsProfileCompletion();
      
      if (needsProfileCompletion) {
        // User needs to complete profile - skip authorization check for now
        const attributes = await fetchUserAttributes();
        
        // Initialize a temporary session for profile completion
        const sessionResponse = await api.initSession(backendTokens, applicationName);
        if (!sessionResponse) {
          throw new Error('Failed to initialize session with SSO backend');
        }
        
        return {
          success: true,
          needsProfileCompletion: true,
          sessionId: sessionResponse.session_id,
          userAttributes: attributes,
          redirectUrl
        };
      }

      // Step 5: Profile is complete, now check authorization
      const userAuth = await api.checkAppUser(backendTokens.id_token, applicationName);
      if (!userAuth) {
        // User not yet authorized for this application - consent needed
        // Return special status indicating consent is needed
        return {
          status: 'consent_required',
          tokens: backendTokens,
          applicationName,
          redirectUrl
        };
      }
      
      // Step 6: Initialize session with SSO backend
      const sessionResponse = await api.initSession(backendTokens, applicationName);
      if (!sessionResponse) {
        throw new Error('Failed to initialize session with SSO backend');
      }

      // Step 7: User is fully authenticated and authorized
      return {
        success: true,
        needsProfileCompletion: false,
        sessionId: sessionResponse.session_id,
        redirectUrl
      };

    } catch (error: any) {
      console.error('Google OAuth process failed:', error);
      throw error;
    }
  }
}

export default new AuthService();
