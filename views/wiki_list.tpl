% rebase('layout', title='All Wikis')
<link rel="stylesheet" href="/static/css/style.css">

<div class="container">
    <div class="dashboard-header">
        <h1>All Wikis</h1>
        <div class="flex items-center gap-4">
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
        <div class="alert alert-error">{{error}}</div>
    % end

    % if not wikis:
        <div class="card text-center py-4">
            <p>No wikis created yet</p>
            % if user and user.can(PermissionSystem.CREATE_WIKI):
                <button class="btn btn-primary mt-2"
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
                    <p>Created by {{wiki.owner_username}}</p>
                    
                    <div class="wiki-meta">
                        <span>{{wiki.created_at[:10]}}</span>
                        % if user and (user.id == wiki.owner_id or user.can(PermissionSystem.MANAGE_WIKI, wiki.id)):
                            <div>
                                <a href="/wikis/{{wiki.slug}}/edit" class="btn btn-sm">
                                    <i class="fas fa-edit"></i>
                                </a>
                                <a href="/wikis/{{wiki.slug}}/delete" class="btn btn-sm btn-danger"
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
    /* Modal styles */
    .modal {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.6);
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
    
    .modal-content {
        background: var(--card-bg);
        border-radius: 12px;
        width: 90%;
        max-width: 600px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
        transform: translateY(-50px);
        transition: transform 0.3s;
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
    
    .modal-body {
        padding: 1.5rem;
    }
    
    .close {
        background: none;
        border: none;
        color: var(--text-color);
        font-size: 2rem;
        cursor: pointer;
        padding: 0 1rem;
    }
    
    /* Wiki grid */
    .wiki-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
        gap: 1.5rem;
    }
    
    .wiki-card {
        background: var(--card-bg);
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: transform 0.3s, box-shadow 0.3s;
    }
    
    .wiki-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 15px rgba(0, 0, 0, 0.1);
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
        color: var(--text-color);
        text-decoration: none;
    }
    
    .wiki-title a:hover {
        color: var(--primary);
    }
    
    .wiki-meta {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-top: 1rem;
        color: var(--text-secondary);
        font-size: 0.9rem;
    }
</style>

<script>
    // Refresh wiki list when a new wiki is created
    document.body.addEventListener('newWikiCreated', function(evt) {
        htmx.ajax('GET', '/wikis', { target: '.container', swap: 'outerHTML' });
    });
</script>
