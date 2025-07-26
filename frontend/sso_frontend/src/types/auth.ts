export interface User {
  sub: string
  email: string
  name?: string
  phone?: string
  gender?: string
}

export interface CognitoTokens {
  id_token: string
  access_token: string
  refresh_token: string
  token_type?: string
  expires_in?: number
}

/**
 * Result from authentication which could be either tokens or an MFA challenge
 */
export type AuthResult = CognitoTokens | MfaChallenge;

/**
 * MFA Challenge response for when MFA verification is required
 */
export interface MfaChallenge {
  challengeName: string;
  session: string;
  challengeParameters?: {
    [key: string]: string;
  };
}

export interface LoginCredentials {
  email: string
  password: string
}

export interface RegisterData {
  email: string
  password: string
  name: string
  phone: string
  gender: string
  accepts_marketing?: boolean
}

export interface AuthError {
  message: string
  code?: string
} 