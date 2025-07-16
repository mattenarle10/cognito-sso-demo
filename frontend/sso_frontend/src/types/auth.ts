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