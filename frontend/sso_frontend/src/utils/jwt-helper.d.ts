/**
 * Parse a JWT token and return the payload as an object
 */
export function parseJwt(token: string): Record<string, any>;

/**
 * Check if a JWT token is expired
 */
export function isTokenExpired(token: string): boolean;
