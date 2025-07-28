<template>
  <div class="admin-container">
    <header class="admin-header">
      <h1>Admin Portal</h1>
      <div class="user-controls">
        <span v-if="currentUser">{{ currentUser.email }}</span>
        <button class="btn-secondary" @click="handleLogout">Logout</button>
      </div>
    </header>

    <div class="search-controls">
      <input 
        type="text" 
        v-model="searchQuery" 
        placeholder="Search users..." 
        class="search-input"
        @keyup.enter="searchUsers"
      />
      <button class="btn-primary" @click="searchUsers">Search</button>
      <button class="btn-secondary" @click="resetSearch">Reset</button>
    </div>

    <div class="loading-indicator" v-if="loading">Loading...</div>
    <div class="error-message" v-if="error">{{ error }}</div>

    <UserTable 
      :users="users" 
      @view-user="openUserModal" 
      @disable-user="confirmDisableUser" 
      @enable-user="confirmEnableUser"
      @reset-password="confirmResetPassword"
      @delete-user="confirmDeleteUser"
    />

    <div class="pagination" v-if="users.length > 0">
      <button 
        class="btn-secondary" 
        @click="loadPreviousPage" 
        :disabled="!hasPreviousPage"
      >
        Previous
      </button>
      <button 
        class="btn-secondary" 
        @click="loadNextPage" 
        :disabled="!paginationToken"
      >
        Next
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
      @confirm="handleConfirmation"
      @cancel="closeConfirmationModal"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, defineProps } from 'vue';
import { useAuth } from '../composables/useAuth';
import { UserService, type User } from '../services/UserService';
import UserTable from '../components/UserTable.vue';
import UserModal from '../components/UserModal.vue';
import ConfirmationModal from '../components/ConfirmationModal.vue';

// Define props
const props = defineProps<{
  currentUser?: { email: string };
  logout?: () => void;
}>();

// Auth
const { userData } = useAuth();
const currentUser = ref(props.currentUser || { email: '' });
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
  const email = user.attributes?.email || user.username;
  confirmationMessage.value = `Are you sure you want to reset the password for ${email}?`;
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

.admin-header h1 {
  margin: 0;
  font-size: 1.75rem;
  font-weight: 600;
  color: #333;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.admin-header h1::before {
  content: '\f013';
  font-family: 'Font Awesome 6 Free';
  font-weight: 900;
}

.user-controls {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.user-controls span {
  font-size: 0.9rem;
  color: #666;
}

.search-controls {
  display: flex;
  gap: 0.75rem;
  margin-bottom: 1.5rem;
  background-color: #f8f8f8;
  padding: 1rem;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.search-input {
  flex-grow: 1;
  padding: 0.6rem 1rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 0.95rem;
  transition: border-color 0.2s;
}

.search-input:focus {
  border-color: #0077cc;
  outline: none;
  box-shadow: 0 0 0 2px rgba(0, 119, 204, 0.1);
  display: flex;
  justify-content: center;
  gap: 8px;
  margin-top: 24px;
  padding-top: 16px;
  border-top: 1px solid var(--border-color);
}

/* Button styles */
.btn-primary, .btn-secondary {
  padding: 8px 16px;
  border-radius: 4px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

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

.btn-secondary:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

@media (max-width: 768px) {
  .admin-container {
    padding: 16px;
  }
  
  .search-controls {
    flex-direction: column;
    align-items: stretch;
  }
  
  .search-input {
    margin-bottom: 8px;
  }
}
</style>
