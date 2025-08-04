import {
  CognitoIdentityProviderClient,
  InitiateAuthCommand,
  SignUpCommand,
  ConfirmSignUpCommand,
  ResendConfirmationCodeCommand,
  GetUserCommand,
  RespondToAuthChallengeCommand,
  SetUserMFAPreferenceCommand,
  ForgotPasswordCommand,
  ConfirmForgotPasswordCommand,
  type InitiateAuthCommandInput,
  type SignUpCommandInput,
  type ConfirmSignUpCommandInput,
  type RespondToAuthChallengeCommandInput,
  type SetUserMFAPreferenceCommandInput,
  type ForgotPasswordCommandInput,
  type ConfirmForgotPasswordCommandInput,
  ChallengeNameType
} from '@aws-sdk/client-cognito-identity-provider'
import { cognitoConfig } from '../config/cognito'

// create cognito client
const cognitoClient = new CognitoIdentityProviderClient({
  region: cognitoConfig.region
})

export interface SignInParams {
  email: string
  password: string
  applicationName?: string
  channelId?: string
}

export interface SignUpParams {
  email: string
  password: string
  phone: string
  name: string
  gender: string
  acceptsMarketing: boolean
  applicationName?: string
  channelId?: string
}

export interface ConfirmSignUpParams {
  email: string
  code: string
  applicationName?: string
  channelId?: string
}

export interface ConfirmSignUpWithPhoneParams extends ConfirmSignUpParams {
  phone: string
}

export interface CognitoTokens {
  access_token: string
  id_token: string
  refresh_token?: string
}

export interface MfaRequiredResponse {
  challengeName: 'SMS_MFA' | 'SOFTWARE_TOKEN_MFA'
  session: string
  challengeParameters?: Record<string, string>
}

// Union type for authentication results
export type AuthResult = CognitoTokens | MfaRequiredResponse

export interface ForgotPasswordParams {
  email: string
  applicationName?: string
  channelId?: string
}

export interface ConfirmForgotPasswordParams {
  email: string
  code: string
  newPassword: string
  applicationName?: string
  channelId?: string
}

class CognitoService {
  async signIn({ email, password, applicationName, channelId }: SignInParams): Promise<AuthResult> {
    const params: InitiateAuthCommandInput = {
      AuthFlow: 'USER_PASSWORD_AUTH',
      ClientId: cognitoConfig.clientId,
      AuthParameters: {
        USERNAME: email,
        PASSWORD: password
      },
      ClientMetadata: {
        application_name: applicationName || '',
        channel_id: channelId || ''
      }
    }

    try {
      const command = new InitiateAuthCommand(params)
      const response = await cognitoClient.send(command)

      // Debug logging to see exactly what's coming back from Cognito
      console.log('[Cognito] Auth response:', {
        ChallengeName: response.ChallengeName,
        Session: !!response.Session, // Just log if it exists to avoid sensitive data
        ChallengeParameters: response.ChallengeParameters,
        AuthenticationResult: !!response.AuthenticationResult
      })

      // Check if MFA challenge is required
      if (response.ChallengeName === 'SMS_MFA' || response.ChallengeName === 'SOFTWARE_TOKEN_MFA') {
        console.log(`[Cognito] ${response.ChallengeName} challenge required`)
        console.log(`[Cognito] Challenge parameters:`, response.ChallengeParameters)
        return {
          challengeName: response.ChallengeName as 'SMS_MFA' | 'SOFTWARE_TOKEN_MFA',
          session: response.Session || '',
          challengeParameters: response.ChallengeParameters
        }
      }

      // Standard authentication result flow
      if (!response.AuthenticationResult) {
        throw new Error('authentication failed')
      }

      const { AccessToken, IdToken, RefreshToken } = response.AuthenticationResult

      if (!AccessToken || !IdToken) {
        throw new Error('missing tokens in response')
      }

      return {
        access_token: AccessToken,
        id_token: IdToken,
        refresh_token: RefreshToken
      }
    } catch (error: any) {
      console.error('cognito signin error:', error)
      throw this.handleCognitoError(error)
    }
  }
  
  /**
   * Verify MFA code after a MFA challenge is received
   */
  async verifyMfa(username: string, mfaCode: string, session: string, challengeName: 'SMS_MFA' | 'SOFTWARE_TOKEN_MFA' = 'SMS_MFA'): Promise<CognitoTokens> {
    // Set up the base parameters
    const params: RespondToAuthChallengeCommandInput = {
      ClientId: cognitoConfig.clientId,
      ChallengeName: challengeName as ChallengeNameType,
      Session: session,
      ChallengeResponses: {
        USERNAME: username
      }
    }
  
    // Add the appropriate challenge response parameter based on challenge type
    if (challengeName === 'SMS_MFA') {
      params.ChallengeResponses!.SMS_MFA_CODE = mfaCode
    } else if (challengeName === 'SOFTWARE_TOKEN_MFA') {
      // For email MFA
      params.ChallengeResponses!.SOFTWARE_TOKEN_MFA_CODE = mfaCode
    }

    try {
      console.log('[Cognito] Sending MFA verification with:', {
        challengeName,
        hasCode: !!mfaCode,
        codeLength: mfaCode.length,
        hasSession: !!session,
        responseParams: params.ChallengeResponses
      })
      
      const command = new RespondToAuthChallengeCommand(params)
      const response = await cognitoClient.send(command)
      
      console.log('[Cognito] MFA verification response:', {
        hasAuthResult: !!response.AuthenticationResult,
        challengeName: response.ChallengeName,
        hasSession: !!response.Session,
        hasTokens: !!(response.AuthenticationResult?.AccessToken)
      })

      if (!response.AuthenticationResult) {
        throw new Error('MFA verification failed')
      }

      const { AccessToken, IdToken, RefreshToken } = response.AuthenticationResult

      if (!AccessToken || !IdToken) {
        throw new Error('missing tokens in response')
      }

      return {
        access_token: AccessToken,
        id_token: IdToken,
        refresh_token: RefreshToken
      }
    } catch (error: any) {
      console.error('MFA verification error:', error)
      throw this.handleCognitoError(error)
    }
  }

  async signUp({ email, password, phone, name, gender, acceptsMarketing, applicationName, channelId }: SignUpParams): Promise<void> {
    const params: SignUpCommandInput = {
      ClientId: cognitoConfig.clientId,
      Username: email,
      Password: password,
      UserAttributes: [
        { Name: 'email', Value: email },
        { Name: 'phone_number', Value: phone },
        { Name: 'name', Value: name },
        { Name: 'gender', Value: gender },
        { Name: 'custom:accepts_marketing', Value: acceptsMarketing.toString() }
      ],
      ClientMetadata: {
        application_name: applicationName || '',
        channel_id: channelId || ''
      }
    }

    try {
      const command = new SignUpCommand(params)
      await cognitoClient.send(command)
    } catch (error: any) {
      console.error('cognito signup error:', error)
      throw this.handleCognitoError(error)
    }
  }

  async confirmSignUp({ email, code, applicationName, channelId }: ConfirmSignUpParams): Promise<void> {
    const params: ConfirmSignUpCommandInput = {
      ClientId: cognitoConfig.clientId,
      Username: email,
      ConfirmationCode: code,
      ClientMetadata: {
        application_name: applicationName || '',
        channel_id: channelId || ''
      }
    }

    try {
      console.log('[Cognito] Confirming signup with params:', JSON.stringify({ ...params, ConfirmationCode: '***' }, null, 2))
      const command = new ConfirmSignUpCommand(params)
      await cognitoClient.send(command)
      // Remove stored UserSub after successful confirmation
      localStorage.removeItem(`cognito_username_${email}`)
      console.log('[Cognito] Signup confirmed successfully')
    } catch (error: any) {
      console.error('[Cognito] confirmSignUp error:', error)
      // Show actual Cognito error for confirmation
      if (error.name === 'NotAuthorizedException' && error.message && error.message.includes('Current status is CONFIRMED')) {
        // User is already confirmed, allow flow to continue
        console.log('[Cognito] User already confirmed, proceeding to login')
        return
      }
      // Map other errors as needed, but show actual message for debugging
      throw new Error(error.message || 'Failed to confirm signup')
    }
  }

  /**
   * Confirm sign up with phone verification code
   * This method is the same as confirmSignUp but emphasizes that it's for phone verification
   */
  async confirmSignUpWithPhone({ email, phone, code, applicationName, channelId }: ConfirmSignUpWithPhoneParams): Promise<void> {
    // In Cognito, phone confirmation uses the same API as email confirmation
    return this.confirmSignUp({ email, code, applicationName, channelId })
  }

  async resendConfirmationCode(email: string): Promise<void> {
    const params = {
      ClientId: cognitoConfig.clientId,
      Username: email
    }

    try {
      const command = new ResendConfirmationCodeCommand(params)
      await cognitoClient.send(command)
    } catch (error: any) {
      console.error('cognito resend code error:', error)
      throw this.handleCognitoError(error)
    }
  }

  /**
   * Resend phone verification code
   * @param phone The phone number to send the code to
   * @param email The user's email address (needed as username)
   */
  async resendPhoneConfirmationCode(phone: string, email: string): Promise<void> {
    // In Cognito, resending phone verification is the same as resending email confirmation
    // The difference is that Cognito will send an SMS instead if phone verification is enabled
    return this.resendConfirmationCode(email)
  }
  
  /**
   * Resend MFA code during login
   * This method re-initiates auth to trigger a new MFA code to be sent
   * @param email User's email address (username)
   * @param password User's password
   * @param applicationName Optional application name for client metadata
   * @param channelId Optional channel ID for client metadata
   * @returns Promise with the new MFA challenge response
   */
  async resendMfaCode({ email, password, applicationName, channelId }: SignInParams): Promise<MfaRequiredResponse> {
    // We essentially call signIn again to trigger a new MFA challenge
    const result = await this.signIn({ email, password, applicationName, channelId })
    
    // Make sure we got an MFA challenge back
    if ('challengeName' in result && result.session) {
      return result as MfaRequiredResponse
    }
    
    throw new Error('Failed to resend MFA code - MFA challenge not triggered')
  }

  /**
   * Set up MFA for an authenticated user
   * @param accessToken The access token from a successful authentication
   * @param mfaType The type of MFA to set up ('sms' or 'software_token')
   * @param enable Whether to enable MFA (true) or disable it (false)
   * @returns Promise<boolean> Whether the operation was successful
   */
  async setupMfa(accessToken: string, mfaType: 'sms' | 'software_token' = 'software_token', enable: boolean = true): Promise<boolean> {
    const params: SetUserMFAPreferenceCommandInput = {
      AccessToken: accessToken
    }

    // Configure MFA settings based on type
    if (mfaType === 'sms') {
      params.SMSMfaSettings = {
        Enabled: enable,
        PreferredMfa: enable
      }
      
      // Explicitly disable software token MFA when SMS is chosen
      params.SoftwareTokenMfaSettings = {
        Enabled: false,
        PreferredMfa: false
      }
    } else {
      // For software token MFA (authenticator apps)
      params.SoftwareTokenMfaSettings = {
        Enabled: enable,
        PreferredMfa: enable
      }
      
      // Explicitly disable SMS MFA when software token is chosen
      params.SMSMfaSettings = {
        Enabled: false,
        PreferredMfa: false
      }
    }

    try {
      const command = new SetUserMFAPreferenceCommand(params)
      await cognitoClient.send(command)
      console.log(`[Cognito] ${mfaType.toUpperCase()} MFA preferences updated:`, enable ? 'enabled' : 'disabled')
      return true
    } catch (error: any) {
      console.error(`[Cognito] Setup ${mfaType.toUpperCase()} MFA error:`, error)
      throw this.handleCognitoError(error)
    }
  }

  /**
   * Initiates the forgot password flow by sending a reset code to the user's email
   * @param email User's email address
   * @param applicationName Optional application name for client metadata
   * @param channelId Optional channel ID for client metadata
   * @returns Promise<void>
   */
  async forgotPassword({ email, applicationName, channelId }: ForgotPasswordParams): Promise<void> {
    const params: ForgotPasswordCommandInput = {
      ClientId: cognitoConfig.clientId,
      Username: email,
      ClientMetadata: {
        application_name: applicationName || '',
        channel_id: channelId || ''
      }
    }

    try {
      const command = new ForgotPasswordCommand(params)
      await cognitoClient.send(command)
      console.log('[Cognito] Forgot password code sent to:', email)
    } catch (error: any) {
      console.error('[Cognito] Forgot password error:', error)
      throw this.handleCognitoError(error)
    }
  }

  /**
   * Confirms the forgot password flow by validating the code and setting a new password
   * @param email User's email address
   * @param code The verification code received via email
   * @param newPassword The new password to set
   * @param applicationName Optional application name for client metadata
   * @param channelId Optional channel ID for client metadata
   * @returns Promise<void>
   */
  async confirmForgotPassword({ email, code, newPassword, applicationName, channelId }: ConfirmForgotPasswordParams): Promise<void> {
    const params: ConfirmForgotPasswordCommandInput = {
      ClientId: cognitoConfig.clientId,
      Username: email,
      ConfirmationCode: code,
      Password: newPassword,
      ClientMetadata: {
        application_name: applicationName || '',
        channel_id: channelId || ''
      }
    }

    try {
      const command = new ConfirmForgotPasswordCommand(params)
      await cognitoClient.send(command)
      console.log('[Cognito] Password reset successful for:', email)
    } catch (error: any) {
      console.error('[Cognito] Confirm forgot password error:', error)
      throw this.handleCognitoError(error)
    }
  }
  
  private handleCognitoError(error: any): Error {
    const errorCode = error.name || error.__type
    
    // Check for password reuse error in message first (Cognito returns this as InvalidParameterException)
    if (error.message && error.message.includes('Password did not conform to policy: Password not in history')) {
      return new Error('You cannot reuse a previous password. Please choose a different password.')
    }
    
    switch (errorCode) {
      case 'NotAuthorizedException':
        return new Error('invalid email or password')
      case 'UserNotFoundException':
        return new Error('user not found')
      case 'UsernameExistsException':
        return new Error('email already exists')
      case 'InvalidPasswordException':
        return new Error('password does not meet requirements')
      case 'CodeMismatchException':
        return new Error('invalid verification code')
      case 'ExpiredCodeException':
        return new Error('verification code has expired')
      case 'LimitExceededException':
        return new Error('too many attempts, please try again later')
      case 'EnableSoftwareTokenMFAException':
        return new Error('failed to enable MFA')
      case 'SoftwareTokenMFANotFoundException':
        return new Error('MFA not set up for this user')
      case 'InvalidParameterException':
        if (error.message && error.message.includes('SMS_MFA_CODE')) {
          return new Error('invalid MFA code')
        }
        return new Error('invalid parameter')
      default:
        return new Error(error.message || 'authentication error occurred')
    }
  }
}

export const cognitoService = new CognitoService() 