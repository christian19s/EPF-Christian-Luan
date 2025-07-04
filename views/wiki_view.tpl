% rebase('layout', title=wiki.name)
<link rel="stylesheet" href="/static/css/style.css">

<div class="container">
    <div class="dashboard-header">
        <h1>{{wiki.name}}</h1>
        
        <div>
            % if user.can(PermissionSystem.CREATE_PAGE, wiki.id):
                <a href="/wikis/{{wiki.slug}}/pages/create" class="btn btn-primary">
                    <i class="fas fa-plus"></i> New Page
                </a>
            % end
            
            % if user.can(PermissionSystem.MANAGE_WIKI, wiki.id):
                <a href="/wikis/{{wiki.slug}}/edit" class="btn">
                    <i class="fas fa-cog"></i> Settings
                </a>
            % end
        </div>
    </div>
    
    % if wiki.description:
        <p class="mb-lg">{{wiki.description}}</p>
    % end
    
    <div class="card">
        <h2 class="section-title">Pages</h2>
        
        % if not pages:
            <div class="text-center py-4">
                <p>No pages created yet</p>
                % if user.can(PermissionSystem.CREATE_PAGE, wiki.id):
                    <a href="/wikis/{{wiki.slug}}/pages/create" class="btn btn-primary mt-2">
                        Create First Page
                    </a>
                % end
            </div>
        % else:
            <ul class="activity-list">
                % for page in pages:
                <li class="activity-item">
                    <div class="activity-icon">
                        <i class="fas fa-file-alt"></i>
                    </div>
                    <div class="activity-content">
                        <div class="activity-title">
                            <a href="/wikis/{{wiki.slug}}/{{page.slug}}">{{page.title}}</a>
                        </div>
                        <div class="activity-time">
                            Last edited: {{page.updated_at[:10]}} by {{page.last_editor.username}}
                        </div>
                    </div>
                </li>
                % end
            </ul>
        % end
    </div>
</div>
