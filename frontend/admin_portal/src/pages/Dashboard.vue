<script setup lang="ts">
import { ref } from 'vue'

// Mock data for dashboard stats
const stats = ref([
  { title: 'TOTAL USERS', value: '245', icon: 'person', trend: '+12%' },
  { title: 'ACTIVE SESSIONS', value: '37', icon: 'key', trend: '+5%' },
  { title: 'APPLICATIONS', value: '3', icon: 'apps', trend: 'N/A' }
])

// Mock data for recent users
const recentUsers = ref([
  { name: 'Matthew Enarle', email: 'matthew.enarle@ecloudvalley.com', role: 'Admin', status: 'Active' },
  { name: 'John Smith', email: 'john.smith@example.com', role: 'User', status: 'Active' },
  { name: 'Jane Doe', email: 'jane.doe@example.com', role: 'User', status: 'Inactive' }
])
</script>

<template>
  <div class="dashboard">
    <header class="dashboard-header">
      <div class="header-title">
        <span class="material-symbols-outlined">dashboard</span>
        <h1>DASHBOARD</h1>
      </div>
      <p class="last-updated">Updated: {{ new Date().toLocaleTimeString() }}</p>
    </header>

    <section class="stats-grid">
      <div v-for="(stat, index) in stats" :key="index" class="stat-card">
        <div class="stat-icon">
          <span class="material-symbols-outlined">{{ stat.icon }}</span>
        </div>
        <div class="stat-info">
          <h3>{{ stat.title }}</h3>
          <div class="stat-value">
            {{ stat.value }}
            <span class="trend">{{ stat.trend }}</span>
          </div>
        </div>
      </div>
    </section>

    <section class="dashboard-section">
      <div class="section-header">
        <div class="section-title">
          <span class="material-symbols-outlined">group</span>
          <h2>RECENT USERS</h2>
        </div>
        <button class="btn-secondary">
          <span>View All</span>
          <span class="material-symbols-outlined">arrow_forward</span>
        </button>
      </div>

      <div class="table-container">
        <table>
          <thead>
            <tr>
              <th>Name</th>
              <th>Email</th>
              <th>Role</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(user, index) in recentUsers" :key="index">
              <td>{{ user.name }}</td>
              <td>{{ user.email }}</td>
              <td>
                <span :class="['badge', user.role === 'Admin' ? 'badge-primary' : 'badge-secondary']">
                  {{ user.role }}
                </span>
              </td>
              <td>
                <span :class="['badge', user.status === 'Active' ? 'badge-success' : 'badge-danger']">
                  {{ user.status }}
                </span>
              </td>
              <td>
                <button class="btn-icon">✏️</button>
                <button class="btn-icon">👁️</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>

    <section class="dashboard-section">
      <div class="section-header">
        <div class="section-title">
          <span class="material-symbols-outlined">admin_panel_settings</span>
          <h2>ADMIN ACTIONS</h2>
        </div>
      </div>
      
      <div class="quick-actions">
        <button class="action-card">
          <div class="action-icon">
            <span class="material-symbols-outlined">person_add</span>
          </div>
          <div class="action-text">Add New User</div>
        </button>
        
        <button class="action-card">
          <div class="action-icon">
            <span class="material-symbols-outlined">monitoring</span>
          </div>
          <div class="action-text">View Reports</div>
        </button>
        
        <button class="action-card">
          <div class="action-icon">
            <span class="material-symbols-outlined">sync</span>
          </div>
          <div class="action-text">Sync Database</div>
        </button>
        
        <button class="action-card">
          <div class="action-icon">
            <span class="material-symbols-outlined">settings</span>
          </div>
          <div class="action-text">System Settings</div>
        </button>
      </div>
    </section>
  </div>
</template>

<style scoped>
.dashboard {
  max-width: 1200px;
  margin: 0 auto;
}

.dashboard-header {
  margin-bottom: 24px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.dashboard-header h1 {
  font-size: 1.8rem;
  font-weight: 700;
  margin: 0;
  color: var(--text-color);
}

.last-updated {
  color: #64748b;
  margin: 0;
  font-size: 0.875rem;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
  margin-bottom: 32px;
}

.stat-card {
  background: var(--card-bg);
  border-radius: 4px;
  padding: 20px;
  border: 1px solid var(--border-color);
  display: flex;
  align-items: center;
}

.stat-icon {
  margin-right: 16px;
  background-color: #f8f8f8;
  width: 50px;
  height: 50px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.stat-icon .material-symbols-outlined {
  font-size: 24px;
  color: var(--secondary-color);
}

.stat-info {
  flex: 1;
}

.stat-info h3 {
  margin: 0 0 8px 0;
  font-size: 0.875rem;
  font-weight: 500;
  color: #64748b;
}

.stat-value {
  font-size: 1.5rem;
  font-weight: 700;
  display: flex;
  align-items: center;
}

.trend {
  font-size: 0.875rem;
  margin-left: 8px;
  color: #10b981;
}

.dashboard-section {
  background: var(--card-bg);
  border-radius: 4px;
  padding: 24px;
  border: 1px solid var(--border-color);
  margin-bottom: 24px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.section-title {
  display: flex;
  align-items: center;
  gap: 8px;
}

.section-title .material-symbols-outlined {
  font-size: 20px;
  color: var(--secondary-color);
}

.section-header h2 {
  font-size: 1rem;
  font-weight: 600;
  margin: 0;
  letter-spacing: 0.5px;
}

.btn-secondary {
  background-color: white;
  border: 1px solid var(--border-color);
  color: var(--text-color);
  padding: 8px 12px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.75rem;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 4px;
}

.btn-secondary:hover {
  border-color: var(--secondary-color);
}

.table-container {
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th, td {
  padding: 12px;
  text-align: left;
  border-bottom: 1px solid var(--border-color);
}

th {
  font-weight: 500;
  color: var(--secondary-color);
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

tbody tr:hover {
  background-color: #f8f8f8;
}

.badge {
  display: inline-block;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 0.7rem;
  font-weight: 500;
  letter-spacing: 0.3px;
}

.badge-primary {
  background-color: #000000;
  color: #ffffff;
}

.badge-secondary {
  background-color: #f1f1f1;
  color: #333333;
}

.badge-success {
  background-color: #e8f5e9;
  color: #1b5e20;
}

.badge-danger {
  background-color: #f5e9e9;
  color: #b71c1c;
}

.btn-icon {
  background: transparent;
  border: none;
  cursor: pointer;
  padding: 4px;
  margin-right: 4px;
  border-radius: 4px;
}

.btn-icon:hover {
  background-color: #f1f5f9;
}

.quick-actions {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 16px;
}

.action-card {
  background-color: var(--card-bg);
  border: 1px solid var(--border-color);
  border-radius: 4px;
  padding: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  cursor: pointer;
  transition: all 0.2s;
}

.action-card:hover {
  border-color: var(--primary-color);
}

.action-icon {
  margin-bottom: 12px;
  background-color: #f8f8f8;
  width: 50px;
  height: 50px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.action-icon .material-symbols-outlined {
  font-size: 24px;
  color: var(--secondary-color);
}

.action-text {
  font-weight: 500;
}
</style>
