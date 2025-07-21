export interface AppValidationResponse {
  valid: boolean
  return_url?: string
  application_id: string
  channel_id: string
}

export interface UserAuthResponse {
  authorized: boolean
  user_id: string
  application_id: string
}

export interface SessionResponse {
  session_id: string
}

export interface TokenResponse {
  session_id: string
  user_id: string
  application_id: string
  tokens: {
    id_token: string
    access_token: string
    refresh_token: string
    token_type: string
    expires_in: number
  }
  expires_at: string
  created_at: string
} 

export interface ApplicationDetails {
  application_id: string
  application_name: string
  application_description?: string
  channels?: Array<{
    channel_id: string
    return_url: string
  }>
  created_at?: string
}

export interface UserSession {
  session_id: string
  user_id: string
  application_id?: string
  application_name?: string
  token_type?: string
  expires_in?: number | null
  device_info?: {
    browser?: string
    os?: string
    device?: string
  }
  is_current?: boolean
  created_at?: string
  last_used_at?: string
  expires_at?: string
}