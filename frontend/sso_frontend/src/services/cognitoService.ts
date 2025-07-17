import {
  CognitoIdentityProviderClient,
  InitiateAuthCommand,
  SignUpCommand,
  ConfirmSignUpCommand,
  ResendConfirmationCodeCommand,
  type InitiateAuthCommandInput,
  type SignUpCommandInput,
  type ConfirmSignUpCommandInput
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

export interface CognitoTokens {
  access_token: string
  id_token: string
  refresh_token?: string
}

class CognitoService {
  async signIn({ email, password, applicationName, channelId }: SignInParams): Promise<CognitoTokens> {
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
      const command = new ConfirmSignUpCommand(params)
      await cognitoClient.send(command)
    } catch (error: any) {
      console.error('cognito confirm signup error:', error)
      throw this.handleCognitoError(error)
    }
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

  private handleCognitoError(error: any): Error {
    const errorCode = error.name || error.__type
    
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
      default:
        return new Error(error.message || 'authentication error occurred')
    }
  }
}

export const cognitoService = new CognitoService() 