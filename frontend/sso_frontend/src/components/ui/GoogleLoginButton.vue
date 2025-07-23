<template>
    <button
      class="google-login-btn"
      @click="loginWithGoogle"
      type="button"
    >
    <img src="../../assets/google-icon.svg" alt="Google" class="icon" />    </button>
  </template>
  
  <script setup lang="ts">
  function loginWithGoogle() {
    const domain = import.meta.env.VITE_COGNITO_DOMAIN
    const clientId = import.meta.env.VITE_COGNITO_CLIENT_ID
    const redirectUri = encodeURIComponent(`${window.location.origin}/auth/callback`)
    // Include email and profile scopes to get user information
    const scopes = encodeURIComponent('openid email profile')
    
    // Add client_metadata to allow pre-signup Lambda to handle missing attributes
    const clientMetadata = encodeURIComponent(JSON.stringify({
      allow_missing_attributes: 'true',
      source: 'google_oauth'
    }))
    
    const url = `${domain}/oauth2/authorize?identity_provider=Google&response_type=CODE&client_id=${clientId}&redirect_uri=${redirectUri}&scope=${scopes}&client_metadata=${clientMetadata}`
    
    console.log('Google login URL:', url)
    console.log('Domain:', domain)
    console.log('Client ID:', clientId)
    console.log('Redirect URI:', redirectUri)
    console.log('Scopes:', scopes)
    console.log('Client Metadata:', clientMetadata)
    
    window.location.href = url
  }
  </script>
  
  <style scoped>
  .google-login-btn {

    gap: 0.5rem;
    color: #222;
    border: 1px solid #4c4c4c;
    border-radius: 6px;
    padding: 0.6rem 1.5rem;
    font-weight: 500;
    font-size: 1rem;
    cursor: pointer;
    transition: box-shadow 0.2s;
  }
  .google-login-btn:hover {
    background-color: #323131;
  }
  .icon {
    width: 20px;
    height: 20px;
  }
  </style>