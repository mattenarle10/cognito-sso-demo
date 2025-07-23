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
      await signInWithRedirect({ provider: 'Google' });
    } catch (err: any) {
      console.error('Error signing in with Google:', err);
      throw err;
    }
  }

  /**
   * Get the current authenticated user
   */
  async getCurrentUser() {
    try {
      return await getCurrentUser();
    } catch (err: any) {
      console.error('Error getting current user:', err);
      return null;
    }
  }

  /**
   * Get current session including tokens
   */
  async getCurrentSession(): Promise<AuthTokens | null> {
    try {
      const session = await fetchAuthSession();
      
      // Check if tokens exist in the session
      if (!session.tokens) {
        console.error('Session tokens are missing');
        return null;
      }
      
      // Safely access token properties with proper type handling
      const idToken = session.tokens.idToken?.toString();
      const accessToken = session.tokens.accessToken?.toString();
      
      // Explicitly handle refreshToken which might be undefined in some flows
      let refreshToken: string | undefined;
      if ('refreshToken' in session.tokens) {
        refreshToken = session.tokens.refreshToken?.toString();
      }
      
      if (!idToken || !accessToken || !refreshToken) {
        console.error('One or more tokens are missing');
        return null;
      }
      
      // Return tokens in the format expected by our AuthTokens interface
      return {
        idToken,
        accessToken,
        refreshToken
      };
    } catch (err: any) {
      console.error('Error getting current session:', err);
      return null;
    }
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
   * This is determined by checking for the custom:needs_profile_completion attribute
   */
  async checkNeedsProfileCompletion(): Promise<boolean> {
    try {
      // First check if we can get a user at all
      const user = await this.getCurrentUser();
      if (!user) return false;
      
      // In Amplify v6, we need to fetch attributes separately
      const attributes = await fetchUserAttributes();
      
      return attributes['custom:needs_profile_completion'] === 'true' || 
             attributes['phone_number'] === '+00000000000';
    } catch (error: any) {
      console.error('Error checking profile completion status:', error);
      return false;
    }
  }
}

export default new AuthService();
