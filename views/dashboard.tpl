% rebase('layout', title='User Dashboard')
<link rel="stylesheet" href="/static/css/dashboard.css">
<script src="/static/js/dark-mode.js"></script>
<script src="/static/js/dashboard.js"></script>

<div class="htmx-indicator">
    <i class="fas fa-spinner fa-spin"></i> Updating profile...
</div>

<div class="dashboard-container">
    % if get('success'):
        <div class="alert alert-success">{{success}}</div>
    % end
    % if get('error'):
        <div class="alert alert-error">{{error}}</div>
    % end
    
    <div class="dashboard-header">
        <h1>Your Dashboard</h1>
        <div class="theme-toggle" id="themeToggle">
            <i class="fas fa-moon"></i>
            <span id="themeText">Dark Mode</span>
        </div>
    </div>
    
    <div class="profile-card">
        <div class="profile-picture-container">
            <img src="{{ user.get_profile_picture_url() }}"
                alt="Profile Picture"
                class="profile-picture"
                id="profileImage">
            
            <form hx-post="/dashboard/update_profile_picture" 
                  hx-encoding="multipart/form-data"
                  hx-target="#profileImage"
                  hx-indicator=".htmx-indicator"
                  id="pictureForm">
                <input type="file"
                    name="profile_picture"
                    id="fileInput"
                    accept="image/*"
                    style="display: none;">
                <button type="button"
                        class="change-picture-btn"
                        onclick="document.getElementById('fileInput').click()">
                    <i class="fas fa-camera"></i>
                </button>
            </form>
        </div>  

        <div class="user-info">
            <h2 class="user-name">{{ user.username }}</h2>
            <p class="user-email">{{ user.email }}</p>
            <p>Member since: {{ user.created_at[:10] }}</p>
            % if user.birthdate:
                <p>Birthdate: {{ user.birthdate }}</p>
            % end
        </div>
        
        <div class="stats-container">
            <div class="stat-card">
                <div class="stat-value">12</div>
                <div class="stat-label">Wikis Created</div>
            </div>
            
            <div class="stat-card">
                <div class="stat-value">47</div>
                <div class="stat-label">Pages Edited</div>
            </div>
            
            <div class="stat-card">
                <div class="stat-value">5</div>
                <div class="stat-label">Collaborations</div>
            </div>
        </div>
        
        <div class="recent-activity">
            <h3 class="section-title">Recent Activity</h3>
            <ul class="activity-list">
                <li class="activity-item">
                    <div class="activity-icon">
                        <i class="fas fa-edit"></i>
                    </div>
                    <div class="activity-content">
                        <div class="activity-title">
                        <div class="activity-time">
                    </div>
                </li>
                
                <li class="activity-item">
                    <div class="activity-icon">
                        <i class="fas fa-plus"></i>
                    </div>
                    <div class="activity-content">
                        <div class="activity-title">Created "API Documentation" page</div>
                        <div class="activity-time">Yesterday</div>
                    </div>
                </li>
                
                <li class="activity-item">
                    <div class="activity-icon">
                        <i class="fas fa-comment"></i>
                    </div>
                    <div class="activity-content">
                        <div class="activity-title">Commented on "Authentication Flow"</div>
                        <div class="activity-time">3 days ago</div>
                    </div>
                </li>
            </ul>
        </div>
    </div>
</div>
