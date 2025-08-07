import { ref } from 'vue';
import type { Ref } from 'vue';
import { parseJwt } from '@/utils/jwt-helper';

/**
 * Composable to check if the current user has admin privileges
 * by examining the JWT token for the custom:is_admin claim
 */
export function useAdminCheck() {
  const isAdmin: Ref<boolean> = ref(false);
  const isCheckingAdmin: Ref<boolean> = ref(false);
  const adminCheckError: Ref<Error | null> = ref(null);

  /**
   * Check if the current user is an admin based on their ID token
   * @param idToken - The user's ID token (optional, will try to get from localStorage if not provided)
   * @returns Whether the user is an admin
   */
  const checkIsAdmin = async (idToken: string | null = null): Promise<boolean> => {
    isCheckingAdmin.value = true;
    adminCheckError.value = null;
    
    try {
      // Get the ID token from localStorage if not provided
      const token = idToken || localStorage.getItem('id_token');
      
      if (!token) {
        isAdmin.value = false;
        return false;
      }
      
      // Parse the JWT token
      const decodedToken = parseJwt(token);
      
      // Check for the custom:is_admin claim
      isAdmin.value = decodedToken['custom:is_admin'] === 'true';
      
      return isAdmin.value;
    } catch (error) {
      console.error('Error checking admin status:', error);
      adminCheckError.value = error as Error;
      isAdmin.value = false;
      return false;
    } finally {
      isCheckingAdmin.value = false;
    }
  };

  /**
   * Redirect to the admin portal if the user is an admin
   * @param adminPortalUrl - The URL of the admin portal
   * @returns Whether the redirection occurred
   */
  const redirectToAdminPortalIfAdmin = async (adminPortalUrl: string): Promise<boolean> => {
    const isUserAdmin = await checkIsAdmin();
    
    if (isUserAdmin) {
      // Get session ID if available in URL or localStorage
      let sessionId = new URLSearchParams(window.location.search).get('session_id');
      if (!sessionId) {
        sessionId = localStorage.getItem('session_id');
      }
      
      // Redirect to admin portal with session_id if available
      const redirectUrl = sessionId 
        ? `${adminPortalUrl}?session_id=${sessionId}` 
        : adminPortalUrl;
      
      window.location.href = redirectUrl;
      return true;
    }
    
    return false;
  };

  return {
    isAdmin,
    isCheckingAdmin,
    adminCheckError,
    checkIsAdmin,
    redirectToAdminPortalIfAdmin
  };
}
