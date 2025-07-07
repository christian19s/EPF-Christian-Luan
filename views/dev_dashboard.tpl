% rebase('layout', title='Dashboard de Usuário')
<link rel="stylesheet" href="/static/css/dashboard.css">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
<script src="https://unpkg.com/htmx.org@1.9.6"></script>
<script src="/static/js/dark-mode.js"></script>

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
        <div class="header-left">
            <a href="/" class="home-button" title="Return to Home">
                <i class="fas fa-home"></i>
            </a>
            <h1>Your Dashboard</h1>
        </div>
        <div class="theme-toggle" id="themeToggle">
            <i class="fas fa-moon"></i>
            <span id="themeText">Dark Mode</span>
        </div>
    </div>
    
    <div class="profile-card">
        <div class="profile-section">
            <div class="profile-picture-container">
                <img src="{{ user.get_profile_picture_url() }}"
                    alt="Profile Picture"
                    class="profile-picture"
                    id="profileImage">
                
                <form hx-post="/dashboard/update_profile_picture" 
                      hx-encoding="multipart/form-data"
                      hx-target="#profileImage"
                      hx-swap="outerHTML"
                      hx-indicator=".htmx-indicator"
                      id="pictureForm">
                    <input type="file"
                        name="profile_picture"
                        id="fileInput"
                        accept="image/jpeg, image/png, image/gif, image/webp"
                        style="display: none;">
                </form>
                <button class="change-picture-btn"
                        onclick="document.getElementById('fileInput').click()">
                    <i class="fas fa-camera"></i>
                </button>
            </div>
            
            <div class="user-info">
                <h2 class="user-name">{{ user.username }}</h2>
                <p class="user-email">{{ user.email }}</p>
                <p class="user-meta">Member since: {{ user.created_at[:10] }}</p>
                <p class="user-meta">Global Role: <span class="role-tag">{{ user.global_role }}</span></p>
                % if user.birthdate:
                    <p class="user-meta">Birthdate: {{ user.birthdate }}</p>
                % end
            </div>
        </div>
        
        <div class="stats-container">
            <div class="stat-card">
                <div class="stat-value">{{ len(user.owned_wikis) }}</div>
                <div class="stat-label">Wikis Created</div>
            </div>
            
            <div class="stat-card">
                <div class="stat-value">{{ len(edited_pages) }}</div>
                <div class="stat-label">Pages Edited</div>
            </div>
            
            <div class="stat-card">
                <div class="stat-value">{{ len(user.wiki_roles) }}</div>
                <div class="stat-label">Collaborations</div>
            </div>
        </div>
        
        <div class="recent-activity">
            <h3 class="section-title">Recent Activity</h3>
            % if edited_pages:
                <ul class="activity-list">
                    % for page in edited_pages:
                    <li class="activity-item">
                        <div class="activity-icon">
                            <i class="fas fa-edit"></i>
                        </div>
                        <div class="activity-content">
                            <div class="activity-title">
                                Edited "{{ page['page_title'] }}" in
                                <a href="/wikis/{{ page['wiki_slug'] }}/{{ page['page_slug'] }}">
                                    {{ page['wiki_name'] }}
                                </a>
                            </div>
                            <div class="activity-time">
                                {{ page['edit_time'] }}
                            </div>
                        </div>
                    </li>
                    % end
                </ul>
            % else:
                <div class="empty-activity">
                    <i class="fas fa-inbox"></i>
                    <p>No recent activity yet</p>
                </div>
            % end
        </div>
    </div>
    
    <div class="account-actions">
        <h3 class="section-title">Account Settings</h3>
        <div class="action-grid">
            <a href="/user/edit" class="action-card">
                <div class="action-icon">
                    <i class="fas fa-user-edit"></i>
                </div>
                <h4>Edit Profile</h4>
                <p>Update your personal information</p>
            </a>
            
            <a href="/change-password" class="action-card">
                <div class="action-icon">
                    <i class="fas fa-lock"></i>
                </div>
                <h4>Change Password</h4>
                <p>Set a new password for your account</p>
            </a>
            
            <a href="/wikis" class="action-card">
                <div class="action-icon">
                    <i class="fas fa-book"></i>
                </div>
                <h4>Your Wikis</h4>
                <p>Manage wikis you created</p>
            </a>
            
            <a href="/logout" class="action-card">
                <div class="action-icon">
                    <i class="fas fa-sign-out-alt"></i>
                </div>
                <h4>Log Out</h4>
                <p>Securely end your session</p>
            </a>
        </div>
    </div>
</div>

<script>
    document.addEventListener('DOMContentLoaded', function() {
        // File input handling
        const fileInput = document.getElementById('fileInput');
        if (fileInput) {
            fileInput.addEventListener('change', function() {
                document.getElementById('pictureForm').requestSubmit();
            });
        }
        
        // Theme change listener
        document.addEventListener('themeChange', function(e) {
            console.log('Theme changed to:', e.detail.mode);
        });
    });
</script>