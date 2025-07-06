% rebase('layout', title=wiki.name)
<link rel="stylesheet" href="/static/css/style.css">

<div class="container">
    <div class="wiki-header">
        <h1>{{wiki.name}}</h1>
        <p class="wiki-description">{{wiki.description}}</p>
        <p>Created by {{wiki.owner_username}} on {{wiki.created_at[:10]}}</p>
        
        % if user and (user.id == wiki.owner_id or user.can(PermissionSystem.MANAGE_WIKI, wiki.id)):
            <div class="wiki-actions">
                <a href="/wikis/{{wiki.slug}}/edit" class="btn btn-sm">
                    <i class="fas fa-edit"></i> Edit Wiki
                </a>
                <a href="/wikis/{{wiki.slug}}/pages/create" class="btn btn-sm btn-primary">
                    <i class="fas fa-plus"></i> New Page
                </a>
            </div>
        % end
    </div>

    % if not pages:
        <div class="card text-center py-4">
            <p>No pages created yet</p>
            % if user and user.can(PermissionSystem.CREATE_PAGE, wiki.id):
                <a href="/wikis/{{wiki.slug}}/pages/create" class="btn btn-primary mt-2">
                    Create First Page
                </a>
            % end
        </div>
    % else:
        <div class="page-list">
            % for page in pages:
            <div class="page-item">
                <h3><a href="/wikis/{{wiki.slug}}/{{page.slug}}">{{page.title}}</a></h3>
                <p>Created on {{page.created_at[:10]}}</p>
            </div>
            % end
        </div>
    % end
</div>

<style>
    .wiki-header {
        margin-bottom: 2rem;
        padding-bottom: 1rem;
        border-bottom: 1px solid var(--surface1);
    }
    
    .wiki-description {
        font-size: 1.1rem;
        color: var(--text-secondary);
        margin-bottom: 1rem;
    }
    
    .wiki-actions {
        display: flex;
        gap: 0.5rem;
        margin-top: 1rem;
    }
    
    .page-list {
        display: grid;
        gap: 1rem;
    }
    
    .page-item {
        background: var(--surface1);
        border-radius: 8px;
        padding: 1.5rem;
        transition: transform 0.2s, box-shadow 0.2s;
    }
    
    .page-item:hover {
        transform: translateY(-3px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    }
    
    .page-item h3 {
        margin-top: 0;
        margin-bottom: 0.5rem;
    }
    
    .page-item h3 a {
        color: var(--text);
        text-decoration: none;
    }
    
    .page-item h3 a:hover {
        color: var(--primary);
    }
</style>
