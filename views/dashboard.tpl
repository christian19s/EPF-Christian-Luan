% rebase('layout', title='User Dashboard')
<link rel="stylesheet" href="/static/css/style.css">
<link rel="stylesheet" href="/static/css/theme.css">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
<script src="https://unpkg.com/htmx.org@1.9.6"></script>
<script src="/static/js/dark-mode.js"></script> <!-- Updated theme manager -->

<style>
    /* Theme-specific adjustments */
    .dark-mode {
        /* Catppuccin Mocha dark theme is applied via JS */
    }
    
    .light-mode {
        /* Gruvbox light theme is applied via JS */
    }
    
    /* Ensure smooth transitions */
    body {
        transition: background-color 0.3s ease, color 0.3s ease;
    }
    
    .dashboard-container {
        max-width: 1200px;
        margin: 0 auto;
        padding: 2rem 1rem;
    }
    
    .dashboard-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 2rem;
        flex-wrap: wrap;
        gap: 1rem;
    }
    
    .theme-toggle {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        cursor: pointer;
        padding: 0.5rem 1rem;
        background-color: var(--surface0);
        border-radius: 50px;
        transition: all 0.3s ease;
    }
    
    .theme-toggle:hover {
        background-color: var(--mauve);
        color: var(--crust);
    }
    
    .profile-card {
        background-color: var(--surface0);
        border-radius: 12px;
        box-shadow: 0 6px 16px rgba(0, 0, 0, 0.2);
        padding: 2rem;
        margin-bottom: 2rem;
        display: grid;
        grid-template-columns: auto 1fr;
        gap: 2rem;
    }
    
    @media (max-width: 768px) {
        .profile-card {
            grid-template-columns: 1fr;
        }
    }
    
    .profile-picture-container {
        position: relative;
        width: 180px;
        height: 180px;
    }
    
    .profile-picture {
        width: 100%;
        height: 100%;
        border-radius: 50%;
        object-fit: cover;
        border: 4px solid var(--mauve);
        transition: border-color 0.3s ease;
    }
    
    .change-picture-btn {
        position: absolute;
        bottom: 10px;
        right: 10px;
        width: 40px;
        height: 40px;
        border-radius: 50%;
        background-color: var(--mauve);
        color: var(--crust);
        border: none;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 2px 10px rgba(0,0,0,0.2);
        transition: all 0.3s ease;
    }
    
    .change-picture-btn:hover {
        background-color: var(--lavender);
        transform: scale(1.1);
    }
    
    .user-info {
        padding-top: 1rem;
    }
    
    .user-name {
        font-size: 2rem;
        margin-bottom: 0.5rem;
        color: var(--text);
    }
    
    .user-email {
        color: var(--subtext0);
        margin-bottom: 1rem;
    }
    
    .role-tag {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        background-color: var(--mauve);
        color: var(--crust);
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
    }
    
    .stats-container {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 1rem;
        margin: 2rem 0;
        grid-column: span 2;
    }
    
    @media (max-width: 768px) {
        .stats-container {
            grid-column: 1;
        }
    }
    
    .stat-card {
        background: linear-gradient(135deg, var(--mauve), var(--lavender));
        color: var(--crust);
        border-radius: 10px;
        padding: 1.5rem;
        text-align: center;
        transition: transform 0.3s ease;
    }
    
    .stat-card:hover {
        transform: translateY(-3px);
    }
    
    .stat-value {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    .stat-label {
        font-size: 1rem;
        opacity: 0.9;
    }
    
    .section-title {
        font-size: 1.5rem;
        margin-bottom: 1.5rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid var(--mauve);
        color: var(--text);
    }
    
    .recent-activity {
        grid-column: span 2;
    }
    
    .activity-list {
        list-style: none;
        padding: 0;
    }
    
    .activity-item {
        display: flex;
        gap: 1rem;
        padding: 1rem;
        border-bottom: 1px solid var(--surface1);
        transition: background-color 0.2s;
    }
    
    .activity-item:hover {
        background-color: var(--surface1);
    }
    
    .activity-icon {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        background-color: var(--surface1);
        color: var(--mauve);
        display: flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
    }
    
    .activity-content {
        flex-grow: 1;
    }
    
    .activity-title {
        font-weight: 600;
        margin-bottom: 0.25rem;
    }
    
    .activity-time {
        font-size: 0.85rem;
        color: var(--subtext0);
    }
    
    .empty-activity {
        text-align: center;
        padding: 2rem;
        color: var(--subtext0);
    }
    
    .empty-activity i {
        font-size: 3rem;
        margin-bottom: 1rem;
        opacity: 0.3;
    }
    
    .account-actions {
        background-color: var(--surface0);
        border-radius: 12px;
        box-shadow: 0 6px 16px rgba(0, 0, 0, 0.2);
        padding: 2rem;
        margin-top: 2rem;
    }
    
    .action-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
        gap: 1.5rem;
    }
    
    .action-card {
        display: block;
        background-color: var(--mantle);
        border-radius: 10px;
        padding: 1.5rem;
        text-align: center;
        transition: all 0.3s ease;
        text-decoration: none;
        color: var(--text);
    }
    
    .action-card:hover {
        transform: translateY(-5px);
        background-color: var(--surface1);
    }
    
    .action-icon {
        width: 60px;
        height: 60px;
        margin: 0 auto 1rem;
        border-radius: 50%;
        background-color: var(--surface1);
        color: var(--mauve);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.5rem;
    }
    
    .action-card h4 {
        margin-bottom: 0.5rem;
        color: var(--text);
    }
    
    .action-card p {
        color: var(--subtext0);
        margin: 0;
    }
    
    .alert {
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1.5rem;
    }
    
    .alert-success {
        background-color: rgba(166, 227, 161, 0.2);
        border: 1px solid var(--green);
        color: var(--green);
    }
    
    .alert-error {
        background-color: rgba(243, 139, 168, 0.2);
        border: 1px solid var(--red);
        color: var(--red);
    }
    
    .htmx-indicator {
        display: none;
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        background: var(--surface0);
        color: var(--text);
        padding: 1rem 2rem;
        border-radius: 8px;
        z-index: 1000;
        box-shadow: 0 4px 20px rgba(0,0,0,0.3);
    }
    
    .htmx-request .htmx-indicator {
        display: block;
    }
</style>

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
            <p>Member since: {{ user.created_at[:10] }}</p>
            <p>Global Role: <span class="role-tag">{{ user.global_role }}</span></p>
            % if user.birthdate:
                <p>Birthdate: {{ user.birthdate }}</p>
            % end
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
            <a href="/profile/edit" class="action-card">
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
    // Handle file input changes
    document.addEventListener('DOMContentLoaded', function() {
        const fileInput = document.getElementById('fileInput');
        if (fileInput) {
            fileInput.addEventListener('change', function() {
                document.getElementById('pictureForm').requestSubmit();
            });
        }
        
        // Listen for theme changes to update UI elements
        document.addEventListener('themeChange', function(e) {
            // Update any theme-specific elements if needed
            console.log('Theme changed to:', e.detail.mode);
        });
    });
</script>
