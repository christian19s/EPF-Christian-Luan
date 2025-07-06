% rebase('layout', title='All Wikis')
<link rel="stylesheet" href="/static/css/style.css">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">

<div class="container">
    <div class="dashboard-header">
        <h1><i class="fas fa-sitemap"></i> All Wikis</h1>
        <div class="header-actions">
            % if user and user.can(PermissionSystem.CREATE_WIKI):
            <button class="btn btn-primary"
                hx-get="/wikis/create/form"
                hx-target="#create-wiki-modal"
                hx-swap="innerHTML"
                _="on htmx:afterOnShow add .show to #create-wiki-modal">
                <i class="fas fa-plus"></i> Create New Wiki
            </button>
            % end
        </div>
    </div>

    % if get('error'):
        <div class="alert alert-error">
            <i class="fas fa-exclamation-circle"></i>
            <div>{{error}}</div>
        </div>
    % end

    % if not wikis:
        <div class="empty-state">
            <i class="fas fa-book-open fa-3x"></i>
            <h3>No wikis created yet</h3>
            <p>Get started by creating your first wiki</p>
            % if user and user.can(PermissionSystem.CREATE_WIKI):
                <button class="btn btn-primary"
                    hx-get="/wikis/create/form"
                    hx-target="#create-wiki-modal"
                    hx-swap="innerHTML"
                    _="on htmx:afterOnShow add .show to #create-wiki-modal">
                    Create First Wiki
                </button>
            % end
        </div>
    % else:
        <div class="wiki-grid">
            % for wiki in wikis:
            <div class="wiki-card">
                <div class="wiki-thumbnail" style="background: linear-gradient(135deg, var(--mauve), var(--lavender));">
                    <i class="fas fa-book"></i>
                </div>
                <div class="wiki-content">
                    <h3 class="wiki-title">
                        <a href="/wikis/{{wiki.slug}}">{{wiki.name}}</a>
                    </h3>
                    <p class="wiki-meta">Created by {{wiki.owner_username}}</p>
                    
                    <div class="wiki-footer">
                        <span class="wiki-date">{{wiki.created_at[:10]}}</span>
                        % if user and (user.id == wiki.owner_id or user.can(PermissionSystem.MANAGE_WIKI, wiki.id)):
                            <div class="wiki-actions">
                                <a href="/wikis/{{wiki.slug}}/edit" class="btn btn-sm btn-icon">
                                    <i class="fas fa-edit"></i>
                                </a>
                                <a href="/wikis/{{wiki.slug}}/delete" class="btn btn-sm btn-icon btn-danger"
                                    onclick="return confirm('Delete this wiki permanently?')">
                                    <i class="fas fa-trash"></i>
                                </a>
                            </div>
                        % end
                    </div>
                </div>
            </div>
            % end
        </div>
    % end
    
    <!-- Modal for creating new wiki -->
    <div id="create-wiki-modal" class="modal" style="display:none;">
        <div class="modal-overlay" _="on click remove .show from #create-wiki-modal then wait 200ms then set #create-wiki-modal's innerHTML to ''"></div>
        <div class="modal-content">
            <div class="modal-header">
                <h3>Create New Wiki</h3>
                <button class="close" _="on click remove .show from #create-wiki-modal then wait 200ms then set #create-wiki-modal's innerHTML to ''">
                    &times;
                </button>
            </div>
            <div class="modal-body">
                <!-- Form will be loaded here by HTMX -->
            </div>
        </div>
    </div>
</div>

<style>
/* Container */
.container {
    max-width: 1200px;
    margin: 2rem auto;
    padding: 0 1rem;
}

.dashboard-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 2rem;
    flex-wrap: wrap;
    gap: 1rem;
    padding: 1.5rem;
    background: var(--surface0);
    border-radius: 12px;
    border: 1px solid var(--surface1);
}

.dashboard-header h1 {
    display: flex;
    align-items: center;
    gap: 12px;
    margin: 0;
    color: var(--subtext1);
}

.header-actions {
    display: flex;
    gap: 0.75rem;
}

/* Alert */
.alert-error {
    display: flex;
    gap: 1rem;
    padding: 1.25rem;
    background: rgba(243, 139, 168, 0.1);
    border-left: 4px solid var(--red);
    color: var(--red);
    align-items: flex-start;
    margin-bottom: 1.5rem;
    border-radius: 8px;
}

.alert-error i {
    font-size: 1.2rem;
    margin-top: 2px;
}

/* Empty state */
.empty-state {
    text-align: center;
    padding: 3rem 2rem;
    background: var(--mantle);
    border-radius: 12px;
    border: 1px dashed var(--surface0);
}

.empty-state i {
    color: var(--overlay0);
    margin-bottom: 1rem;
}

.empty-state h3 {
    margin: 0 0 0.5rem;
    color: var(--subtext1);
}

.empty-state p {
    color: var(--subtext0);
    margin-bottom: 1.5rem;
}

/* Wiki grid */
.wiki-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 1.5rem;
}

.wiki-card {
    background: var(--mantle);
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    transition: transform 0.3s, box-shadow 0.3s;
    border: 1px solid var(--surface0);
}

.wiki-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 10px 15px rgba(0, 0, 0, 0.1);
    border-color: var(--surface1);
}

.wiki-thumbnail {
    height: 150px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-size: 3rem;
}

.wiki-content {
    padding: 1.5rem;
}

.wiki-title {
    margin-top: 0;
    margin-bottom: 0.5rem;
}

.wiki-title a {
    color: var(--subtext1);
    text-decoration: none;
    transition: color 0.2s;
}

.wiki-title a:hover {
    color: var(--blue);
    text-decoration: underline;
}

.wiki-meta {
    color: var(--subtext0);
    font-size: 0.9rem;
    margin-bottom: 1rem;
}

.wiki-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.wiki-date {
    font-size: 0.85rem;
    color: var(--subtext0);
}

.wiki-actions {
    display: flex;
    gap: 0.5rem;
}

.btn-icon {
    padding: 0.5rem;
    border-radius: 6px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    background: transparent;
    border: 1px solid var(--surface1);
    color: var(--subtext0);
    cursor: pointer;
    transition: all 0.2s;
}

.btn-icon:hover {
    background: var(--surface0);
    color: var(--text);
}

.btn-danger:hover {
    color: var(--red);
    border-color: rgba(243, 139, 168, 0.3);
    background: rgba(243, 139, 168, 0.1);
}

/* Modal styles */
.modal {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1000;
    opacity: 0;
    transition: opacity 0.3s;
    pointer-events: none;
}

.modal.show {
    opacity: 1;
    pointer-events: auto;
}

.modal-overlay {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.6);
}

.modal-content {
    background: var(--mantle);
    border-radius: 12px;
    width: 90%;
    max-width: 600px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
    transform: translateY(-50px);
    transition: transform 0.3s;
    position: relative;
    z-index: 2;
    border: 1px solid var(--surface0);
}

.modal.show .modal-content {
    transform: translateY(0);
}

.modal-header {
    padding: 1.5rem;
    border-bottom: 1px solid var(--surface1);
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.modal-header h3 {
    margin: 0;
    color: var(--subtext1);
}

.close {
    background: none;
    border: none;
    color: var(--text);
    font-size: 1.5rem;
    cursor: pointer;
    padding: 0 0.5rem;
}

.modal-body {
    padding: 1.5rem;
}

/* Button styles */
.btn {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.65rem 1.25rem;
    border-radius: 6px;
    font-weight: 500;
    transition: all 0.2s ease;
    border: none;
    cursor: pointer;
    text-decoration: none;
    font-size: 0.95rem;
}

.btn-primary {
    background-color: var(--green);
    color: var(--crust);
}

.btn-primary:hover {
    background-color: #94d68c;
}

.btn-sm {
    padding: 0.5rem 1rem;
    font-size: 0.9rem;
}
</style>

<script>
    // Refresh wiki list when a new wiki is created
    document.body.addEventListener('newWikiCreated', function(evt) {
        htmx.ajax('GET', '/wikis', { target: '.container', swap: 'outerHTML' });
    });
    
    // Initialize theme manager
    document.addEventListener('DOMContentLoaded', ThemeManager.init);
</script>
