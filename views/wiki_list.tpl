% rebase('layout', title='All Wikis')
<link rel="stylesheet" href="/static/css/style.css">

<div class="container">
    <div class="dashboard-header">
        <h1>All Wikis</h1>
        % if user.can(PermissionSystem.CREATE_PAGE):
            <a href="/wikis/create" class="btn btn-primary">
                <i class="fas fa-plus"></i> Create New Wiki
            </a>
        % end
    </div>

    % if get('error'):
        <div class="alert alert-error">{{error}}</div>
    % end

    <div class="wiki-grid">
        % for wiki in wikis:
        <div class="wiki-card">
            <div class="wiki-thumbnail">
                <i class="fas fa-book"></i>
            </div>
            <div class="wiki-content">
                <h3 class="wiki-title">
                    <a href="/wikis/{{wiki.slug}}">{{wiki.name}}</a>
                </h3>
                <p>Created by {{wiki.owner.username}}</p>
                <p>{{len(wiki.pages)}} pages</p>
                
                <div class="wiki-meta">
                    <span>{{wiki.created_at[:10]}}</span>
                    % if user.id == wiki.owner_id or user.is_admin():
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
</div>
