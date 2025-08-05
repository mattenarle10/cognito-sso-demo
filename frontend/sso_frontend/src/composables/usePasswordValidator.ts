import { ref } from 'vue'

interface ValidationResult {
  valid: boolean
  message: string
}

export function usePasswordValidator() {
  // Password validation rules
  const validatePassword = (password: string): ValidationResult => {
    // Check length
    if (password.length < 8) {
      return {
        valid: false,
        message: 'Password must be at least 8 characters long'
      }
    }

    // Check for uppercase letter
    if (!/[A-Z]/.test(password)) {
      return {
        valid: false,
        message: 'Password must contain at least one uppercase letter'
      }
    }

    // Check for lowercase letter
    if (!/[a-z]/.test(password)) {
      return {
        valid: false,
        message: 'Password must contain at least one lowercase letter'
      }
    }

    // Check for number
    if (!/[0-9]/.test(password)) {
      return {
        valid: false,
        message: 'Password must contain at least one number'
      }
    }

    // Check for special character
    if (!/[^A-Za-z0-9]/.test(password)) {
      return {
        valid: false,
        message: 'Password must contain at least one special character'
      }
    }

    // All checks passed
    return {
      valid: true,
      message: 'Password meets all requirements'
    }
  }

  return {
    validatePassword
  }
}
