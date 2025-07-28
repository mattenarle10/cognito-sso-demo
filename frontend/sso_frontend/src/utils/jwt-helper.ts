/**
 * Parse a JWT token and return the payload as an object
 * @param token - JWT token to parse
 * @returns Decoded JWT payload
 */
export function parseJwt(token: string): Record<string, any> {
  try {
    // Get the payload part of the JWT (second part)
    const base64Url = token.split('.')[1];
    const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
    
    // Decode the base64 string
    const jsonPayload = decodeURIComponent(
      atob(base64)
        .split('')
        .map(c => '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2))
        .join('')
    );

    return JSON.parse(jsonPayload);
  } catch (error) {
    console.error('Error parsing JWT token:', error);
    return {};
  }
}

/**
 * Check if a JWT token is expired
 * @param token - JWT token to check
 * @returns Whether the token is expired
 */
export function isTokenExpired(token: string): boolean {
  try {
    const decoded = parseJwt(token);
    const currentTime = Math.floor(Date.now() / 1000);
    
    // Check if token has an expiration time and if it's in the past
    return decoded.exp && decoded.exp < currentTime;
  } catch (error) {
    console.error('Error checking token expiration:', error);
    return true; // Assume expired on error
  }
}
