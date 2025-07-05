% rebase('layout', title='All Wikis')
<link rel="stylesheet" href="/static/css/theme.css">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
<script src="https://unpkg.com/htmx.org@1.9.6"></script>
<script src="https://unpkg.com/hyperscript.org@0.9.11"></script>

<div class="container">
    <div class="dashboard-header">
        <h1>All Wikis</h1>
        % if user and user.can.create_wiki():
            <button class="btn btn-primary"
                hx-get="/wikis/create/form"
                hx-target="#create-wiki-modal"
                hx-swap="innerHTML"
                _="on htmx:afterOnShow add .show to #create-wiki-modal">
                <i class="fas fa-plus"></i> Create New Wiki
            </button>
        % end
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
    }
    
    .modal.show {
        opacity: 1;
        display: flex;
    }
    
    .modal-content {
        background: var(--surface0);
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
        color: var(--text);
        font-size: 2rem;
        cursor: pointer;
        padding: 0 1rem;
    }
</style>

<script>
    // Refresh wiki list when a new wiki is created
    document.body.addEventListener('newWikiCreated', function(evt) {
        htmx.ajax('GET', '/wikis', { target: '.container', swap: 'outerHTML' });
    });
</script>
