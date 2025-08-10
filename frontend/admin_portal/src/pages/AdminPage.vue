<template>
  <div class="admin-container">
    <header class="admin-header">
      <div class="header-title">
        <svg class="header-icon" viewBox="0 0 24 24" aria-hidden="true">
          <path fill="currentColor" d="M19.14,12.94 C19.19,12.64 19.22,12.33 19.22,12 C19.22,11.67 19.19,11.36 19.14,11.06 L21.19,9.47 C21.37,9.33 21.42,9.08 21.32,8.87 L19.32,5.13 C19.21,4.92 18.96,4.84 18.74,4.91 L16.3,5.8 C15.79,5.41 15.22,5.09 14.6,4.85 L14.24,2.25 C14.21,2.03 14.02,1.87 13.8,1.87 L10.2,1.87 C9.98,1.87 9.79,2.03 9.76,2.25 L9.4,4.85 C8.78,5.09 8.21,5.41 7.7,5.8 L5.26,4.91 C5.04,4.83 4.79,4.92 4.68,5.13 L2.68,8.87 C2.58,9.08 2.63,9.33 2.81,9.47 L4.86,11.06 C4.81,11.36 4.78,11.67 4.78,12 C4.78,12.33 4.81,12.64 4.86,12.94 L2.81,14.53 C2.63,14.67 2.58,14.92 2.68,15.13 L4.68,18.87 C4.79,19.08 5.04,19.16 5.26,19.09 L7.7,18.2 C8.21,18.59 8.78,18.91 9.4,19.15 L9.76,21.75 C9.79,21.97 9.98,22.13 10.2,22.13 L13.8,22.13 C14.02,22.13 14.21,21.97 14.24,21.75 L14.6,19.15 C15.22,18.91 15.79,18.59 16.3,18.2 L18.74,19.09 C18.96,19.17 19.21,19.08 19.32,18.87 L21.32,15.13 C21.42,14.92 21.37,14.67 21.19,14.53 L19.14,12.94 Z M12,15.5 C10.07,15.5 8.5,13.93 8.5,12 C8.5,10.07 10.07,8.5 12,8.5 C13.93,8.5 15.5,10.07 15.5,12 C15.5,13.93 13.93,15.5 12,15.5 Z"/>
        </svg>
        <div>
          <h1>Admin Portal</h1>
          <p class="subtitle">Manage users and account settings</p>
        </div>
      </div>
      <div class="user-controls">
        <div v-if="currentUser?.email" class="user-chip">
          <div class="avatar" :title="currentUser.email">{{ userInitial }}</div>
          <span class="user-email">{{ currentUser.email }}</span>
        </div>
        <button class="btn-secondary btn-icon" @click="handleLogout" aria-label="Logout">
          <svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M10,17V14H3V10H10V7L15,12L10,17M19,3A2,2 0 0,1 21,5V19A2,2 0 0,1 19,21H12A2,2 0 0,1 10,19V17H12V19H19V5H12V7H10V5A2,2 0 0,1 12,3H19Z"/></svg>
          <span>Logout</span>
        </button>
      </div>
    </header>

    <div class="toolbar">
      <div class="search-group">
        <svg class="search-icon" viewBox="0 0 24 24" aria-hidden="true">
          <path fill="currentColor" d="M9.5,3A6.5,6.5 0 0,1 16,9.5C16,11.11 15.41,12.59 14.41,13.73L20.31,19.63L18.9,21.04L13,15.14C11.86,16.14 10.38,16.73 8.77,16.73A6.5,6.5 0 0,1 2.27,10.23A6.5,6.5 0 0,1 8.77,3.73A6.5,6.5 0 0,1 9.5,3M9.5,5A4.5,4.5 0 0,0 5,9.5A4.5,4.5 0 0,0 9.5,14A4.5,4.5 0 0,0 14,9.5A4.5,4.5 0 0,0 9.5,5Z"/>
        </svg>
        <input 
          type="text"
          v-model="searchQuery"
          placeholder="Search by email..."
          class="search-input"
          @keyup.enter="searchUsers"
          aria-label="Search users by email"
        />
      </div>
      <div class="toolbar-actions">
        <button class="btn-primary btn-icon" @click="searchUsers">
          <svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M9,2A7,7 0 0,1 16,9C16,10.79 15.37,12.42 14.32,13.68L21.61,20.97L20.2,22.38L12.91,15.09C11.65,16.14 10.02,16.77 8.23,16.77A7,7 0 0,1 1.23,9.77A7,7 0 0,1 8.23,2.77A7,7 0 0,1 9,2M9,4A5,5 0 0,0 4,9A5,5 0 0,0 9,14A5,5 0 0,0 14,9A5,5 0 0,0 9,4Z"/></svg>
          <span>Search</span>
        </button>
        <button class="btn-secondary btn-icon" @click="resetSearch">
          <svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M12,5V2L8,6L12,10V7C15.31,7 18,9.69 18,13C18,13.65 17.89,14.27 17.69,14.84L19.17,16.32C19.69,15.29 20,14.17 20,13C20,8.58 16.42,5 12,5M6.31,9.16C5.8,10.19 5.5,11.31 5.5,12.5C5.5,16.08 8.08,18.83 11.5,19V22L15.5,18L11.5,14V17C9,16.83 7,14.73 7,12.5C7,11.38 7.39,10.36 8.05,9.55L6.31,9.16Z"/></svg>
          <span>Reset</span>
        </button>
      </div>
    </div>

    <div class="meta-row" v-if="users.length > 0 || searchQuery">
      <span class="meta-item">
        <svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M12,20A8,8 0 1,0 4,12A8,8 0 0,0 12,20M11,6H13V13H11V6M11,16H13V18H11V16Z"/></svg>
        {{ users.length }} results
      </span>
      <button v-if="searchQuery" class="link-button" @click="resetSearch">
        <svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z"/></svg>
        Clear filter
      </button>
    </div>

    <div class="loading-indicator" v-if="loading">
      <div class="spinner"></div>
      <span>Loading...</span>
    </div>
    <div class="error-message" v-if="error">{{ error }}</div>

    <UserTable 
      :users="users" 
      @view-user="openUserModal" 
      @disable-user="confirmDisableUser" 
      @enable-user="confirmEnableUser"
      @reset-password="confirmResetPassword"
      @change-name="confirmChangeName"
      @delete-user="confirmDeleteUser"
    />

    <div class="pagination" v-if="users.length > 0">
      <button 
        class="btn-secondary btn-icon" 
        @click="loadPreviousPage" 
        :disabled="!hasPreviousPage"
      >
        <svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M20,11V13H8L13.5,18.5L12.08,19.92L4.16,12L12.08,4.08L13.5,5.5L8,11H20Z"/></svg>
        <span>Previous</span>
      </button>
      <button 
        class="btn-secondary btn-icon" 
        @click="loadNextPage" 
        :disabled="!paginationToken"
      >
        <span>Next</span>
        <svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M4,11V13H16L10.5,18.5L11.92,19.92L19.84,12L11.92,4.08L10.5,5.5L16,11H4Z"/></svg>
      </button>
    </div>

    <!-- Modals -->
    <UserModal 
      :is-open="userModalOpen" 
      :user="selectedUser" 
      @close="closeUserModal"
    />

    <ConfirmationModal
      :is-open="confirmationModalOpen"
      :title="confirmationTitle"
      :message="confirmationMessage"
      :confirm-text="confirmationButtonText"
      :loading="loading"
      @confirm="handleConfirmation"
      @cancel="closeConfirmationModal"
    />
    
    <EditUserNameModal
      :is-open="editNameModalOpen"
      :user="selectedUser"
      @cancel="closeEditNameModal"
      @saved="handleNameUpdated"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, defineProps, computed } from 'vue';
import { useAuth } from '../composables/useAuth';
import { UserService, type User } from '../services/UserService';
import UserTable from '../components/UserTable.vue';
import UserModal from '../components/UserModal.vue';
import ConfirmationModal from '../components/ConfirmationModal.vue';
import EditUserNameModal from '../components/EditUserNameModal.vue';

// Define props
const props = defineProps<{
  currentUser?: { email: string };
  logout?: () => void;
}>();

// Auth
const { userData } = useAuth();
const currentUser = ref(props.currentUser || { email: '' });
const userInitial = computed(() => (currentUser.value?.email?.[0] || '?').toUpperCase());
const handleLogout = () => {
  if (props.logout) {
    props.logout();
  }
};

// State
const users = ref<User[]>([]);
const loading = ref(false);
const error = ref('');
const paginationToken = ref<string | null>(null);
const paginationHistory = ref<string[]>([]);
const searchQuery = ref('');

// Modal state
const userModalOpen = ref(false);
const selectedUser = ref<User | null>(null);
const confirmationModalOpen = ref(false);
const editNameModalOpen = ref(false);
const confirmationTitle = ref('');
const confirmationMessage = ref('');
const confirmationButtonText = ref('');
const confirmationAction = ref<() => Promise<void>>(() => Promise.resolve());

// Computed
const hasPreviousPage = ref(false);

// Lifecycle
onMounted(async () => {
  await loadUsers();
});

// Methods
async function loadUsers(token: string | null = null) {
  loading.value = true;
  error.value = '';
  
  try {
    const params: { pagination_token?: string; filter?: string } = {};
    
    if (token) {
      params.pagination_token = token;
    }
    
    if (searchQuery.value) {
      params.filter = `email = "${searchQuery.value}"`;
    }
    
    const response = await UserService.getUsers(params);
    users.value = response.users;
    paginationToken.value = response.pagination_token || null;
    
    // Update pagination history for "previous" functionality
    if (!token) {
      paginationHistory.value = [];
      hasPreviousPage.value = false;
    }
    
  } catch (err: any) {
    error.value = err.message || 'Failed to load users';
  } finally {
    loading.value = false;
  }
}

async function loadNextPage() {
  if (paginationToken.value) {
    // Save current token for "previous" functionality
    paginationHistory.value.push(paginationToken.value);
    hasPreviousPage.value = true;
    
    await loadUsers(paginationToken.value);
  }
}

async function loadPreviousPage() {
  if (paginationHistory.value.length > 0) {
    // Pop the last token and use the one before it
    paginationHistory.value.pop();
    const previousToken = paginationHistory.value.length > 0 
      ? paginationHistory.value[paginationHistory.value.length - 1] 
      : null;
    
    hasPreviousPage.value = paginationHistory.value.length > 0;
    await loadUsers(previousToken);
  }
}

async function searchUsers() {
  await loadUsers();
}

function resetSearch() {
  searchQuery.value = '';
  loadUsers();
}

// Modal functions
function openUserModal(user: User) {
  selectedUser.value = user;
  userModalOpen.value = true;
}

function closeUserModal() {
  userModalOpen.value = false;
  selectedUser.value = null;
}

// Confirmation modal functions
function confirmDisableUser(user: User) {
  selectedUser.value = user;
  confirmationTitle.value = 'Disable User';
  const email = user.attributes?.email || user.username;
  confirmationMessage.value = `Are you sure you want to disable ${email}?`;
  confirmationButtonText.value = 'Disable';
  confirmationAction.value = disableUser;
  confirmationModalOpen.value = true;
}

function confirmEnableUser(user: User) {
  selectedUser.value = user;
  confirmationTitle.value = 'Enable User';
  const email = user.attributes?.email || user.username;
  confirmationMessage.value = `Are you sure you want to enable ${email}?`;
  confirmationButtonText.value = 'Enable';
  confirmationAction.value = enableUser;
  confirmationModalOpen.value = true;
}

function confirmResetPassword(user: User) {
  selectedUser.value = user;
  confirmationTitle.value = 'Reset Password';
  confirmationMessage.value = `Are you sure you want to reset the password for ${user.username}? The user will receive an email with a verification code to set a new password.`;
  confirmationButtonText.value = 'Reset Password';
  confirmationAction.value = resetPassword;
  confirmationModalOpen.value = true;
}

function confirmDeleteUser(user: User) {
  selectedUser.value = user;
  confirmationTitle.value = 'Delete User';
  const email = user.attributes?.email || user.username;
  confirmationMessage.value = `Are you sure you want to permanently delete ${email}? This action cannot be undone.`;
  confirmationButtonText.value = 'Delete';
  confirmationAction.value = deleteUser;
  confirmationModalOpen.value = true;
}

function closeConfirmationModal() {
  confirmationModalOpen.value = false;
}

async function handleConfirmation() {
  await confirmationAction.value();
  closeConfirmationModal();
}

// User actions
async function disableUser() {
  if (!selectedUser.value) return;
  
  loading.value = true;
  try {
    await UserService.disableUser(selectedUser.value.username);
    // Refresh user list
    await loadUsers();
  } catch (err: any) {
    error.value = err.message || 'Failed to disable user';
  } finally {
    loading.value = false;
  }
}

async function enableUser() {
  if (!selectedUser.value) return;
  
  loading.value = true;
  try {
    await UserService.enableUser(selectedUser.value.username);
    // Refresh user list
    await loadUsers();
  } catch (err: any) {
    error.value = err.message || 'Failed to enable user';
  } finally {
    loading.value = false;
  }
}

async function resetPassword() {
  if (!selectedUser.value) return;
  
  loading.value = true;
  try {
    await UserService.resetPassword(selectedUser.value.username);
    error.value = ''; // Clear any previous errors
  } catch (err: any) {
    error.value = err.message || 'Failed to reset password';
  } finally {
    loading.value = false;
  }
}

async function deleteUser() {
  if (!selectedUser.value) return;
  
  loading.value = true;
  try {
    await UserService.deleteUser(selectedUser.value.username);
    // Refresh user list
    await loadUsers();
  } catch (err: any) {
    error.value = err.message || 'Failed to delete user';
  } finally {
    loading.value = false;
  }
}

// Name editing functions
function confirmChangeName(user: User) {
  selectedUser.value = user;
  editNameModalOpen.value = true;
}

function closeEditNameModal() {
  editNameModalOpen.value = false;
}

async function handleNameUpdated() {
  // Close the modal
  editNameModalOpen.value = false;
  // Refresh user list to show updated name
  await loadUsers();
}
</script>

<style scoped>
.admin-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.admin-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #eee;
}

.header-title { display: flex; align-items: center; gap: 12px; }
.header-icon { width: 36px; height: 36px; color: var(--primary-color); }
.admin-header h1 { margin: 0; font-size: 1.5rem; font-weight: 700; color: #1f2937; }
.subtitle { margin: 2px 0 0 0; font-size: 0.95rem; color: #6b7280; }

.user-controls {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.user-chip { display: flex; align-items: center; gap: 10px; background: #f3f4f6; border: 1px solid #e5e7eb; padding: 6px 10px; border-radius: 999px; }
.avatar { width: 28px; height: 28px; border-radius: 50%; background: #e0e7ff; color: #3730a3; display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 0.9rem; }
.user-email { font-size: 0.9rem; color: #374151; }

.toolbar { display: flex; justify-content: space-between; gap: 12px; margin-bottom: 1rem; align-items: center; flex-wrap: wrap; }
.search-group { flex: 1; display: flex; align-items: center; gap: 8px; background: #f9fafb; border: 1px solid #e5e7eb; padding: 8px 10px; border-radius: 8px; }
.search-icon { width: 18px; height: 18px; color: #6b7280; }

.search-input {
  flex: 1;
  padding: 6px 8px;
  border: none;
  background: transparent;
  font-size: 0.95rem;
}

.search-input:focus {
  outline: none;
}

/* Button styles */
.btn-primary, .btn-secondary { padding: 8px 14px; border-radius: 8px; font-size: 14px; font-weight: 600; cursor: pointer; transition: all 0.2s; display: inline-flex; align-items: center; gap: 8px; }
.btn-icon svg { width: 18px; height: 18px; }

.btn-primary {
  background-color: var(--primary-color);
  color: white;
  border: none;
}

.btn-secondary {
  background-color: white;
  border: 1px solid var(--border-color);
  color: var(--text-color);
}

.btn-primary:hover {
  background-color: var(--secondary-color);
}

.btn-secondary:hover {
  border-color: var(--primary-color);
}

.btn-secondary:disabled, .btn-danger:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.link-button { display: inline-flex; align-items: center; gap: 6px; background: transparent; border: none; color: var(--primary-color); cursor: pointer; padding: 4px 6px; font-weight: 600; }
.link-button svg { width: 16px; height: 16px; }

.meta-row { display: flex; align-items: center; justify-content: space-between; margin: 6px 0 12px; color: #6b7280; font-size: 0.9rem; }
.meta-item { display: inline-flex; align-items: center; gap: 6px; }
.meta-item svg { width: 16px; height: 16px; color: #6b7280; }

/* Loading indicator styles */
.loading-indicator {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1rem;
  background-color: #f9fafb;
  border-radius: 4px;
  margin-bottom: 1rem;
  color: #495057;
  font-weight: 500;
}

.spinner {
  width: 24px;
  height: 24px;
  border: 3px solid rgba(0, 119, 204, 0.2);
  border-radius: 50%;
  border-top-color: #0077cc;
  animation: spin 1s ease-in-out infinite;
  margin-right: 0.75rem;
}

.spinner-small {
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  border-top-color: #ffffff;
  animation: spin 1s ease-in-out infinite;
  display: inline-block;
  margin-right: 0.5rem;
  vertical-align: middle;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.error-message {
  background-color: #fff5f5;
  color: #e03131;
  padding: 0.75rem 1rem;
  border-radius: 4px;
  margin-bottom: 1rem;
  border-left: 4px solid #e03131;
  font-weight: 500;
}

.pagination { display: flex; justify-content: flex-end; gap: 8px; margin-top: 12px; }

@media (max-width: 768px) {
  .admin-container {
    padding: 16px;
  }
  .toolbar { flex-direction: column; align-items: stretch; }
  .toolbar-actions { display: flex; gap: 8px; }
  .search-input {
    margin-bottom: 8px;
  }
}
</style>
