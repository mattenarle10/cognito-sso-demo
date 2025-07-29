import { api } from './api';

export interface User {
  username: string;
  user_status: string;
  enabled: boolean;
  user_create_date: string;
  user_last_modified_date: string;
  attributes?: {
    name?: string;
    email?: string;
    phone_number?: string;
    'email_verified'?: string;
    'phone_number_verified'?: string;
    gender?: string;
    'custom:accepts_marketing'?: string;
    sub?: string;
    [key: string]: any;
  };
  [key: string]: any;
}

export interface PaginatedResponse {
  users: User[];
  pagination_token?: string;
}

export class UserService {
  /**
   * Get a list of users with optional pagination
   */
  static async getUsers(params: { limit?: number; pagination_token?: string; filter?: string } = {}): Promise<PaginatedResponse> {
    return api.getUsers(params);
  }

  /**
   * Get detailed information for a specific user
   */
  static async getUserDetails(userId: string): Promise<User> {
    return api.getUserDetails(userId);
  }

  /**
   * Disable a user account
   */
  static async disableUser(userId: string): Promise<any> {
    return api.disableUser(userId);
  }

  /**
   * Enable a user account
   */
  static async enableUser(userId: string): Promise<any> {
    return api.enableUser(userId);
  }

  /**
   * Reset a user's password
   */
  static async resetPassword(userId: string): Promise<any> {
    return api.resetPassword(userId);
  }

  /**
   * Delete a user account
   */
  static async deleteUser(userId: string): Promise<any> {
    return api.deleteUser(userId);
  }

  /**
   * Update user attributes (e.g., name, phone number)
   */
  static async updateUser(userId: string, attributes: Record<string, string>): Promise<any> {
    return api.updateUser(userId, attributes);
  }
}
