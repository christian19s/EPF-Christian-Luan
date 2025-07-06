% rebase('layout', title='Wiki Categories')
<link rel="stylesheet" href="/static/css/style.css">

<div class="container">
    <div class="header">
        <h1><i class="fas fa-tags"></i> Wiki Categories</h1>
    </div>

    % if not categories:
        <div class="empty-state">
            <i class="fas fa-folder-open fa-2x"></i>
            <p>No categories available</p>
        </div>
    % else:
        <div class="category-grid">
            % for category in categories:
            <div class="category-card" style="border-left: 4px solid {{category['color']}}">
                <div class="category-header">
                    <i class="fas fa-{{category['icon']}}" style="color: {{category['color']}}"></i>
                    <h2>{{category['name']}}</h2>
                    <span class="badge">{{len(category['wikis'])}} wiki{{'s' if len(category['wikis']) != 1 else ''}}</span>
                </div>
                
                % if category['wikis']:
                <ul class="wiki-list">
                    % for wiki in category['wikis']:
                    <li>
                        <a href="/wikis/{{wiki['slug']}}">
                            <i class="fas fa-book"></i> {{wiki['name']}}
                        </a>
                        <small>by {{wiki['owner_username']}}</small>
                    </li>
                    % end
                </ul>
                % else:
                <p class="empty">No wikis in this category</p>
                % end
            </div>
            % end
        </div>
    % end
</div>

<style>
    .category-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
        gap: 1.5rem;
    }
    
    .category-card {
        background: var(--surface0);
        border-radius: 8px;
        padding: 1.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .category-header {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        margin-bottom: 1rem;
    }
    
    .category-header i {
        font-size: 1.5rem;
    }
    
    .category-header h2 {
        margin: 0;
        flex-grow: 1;
    }
    
    .badge {
        background: var(--surface1);
        padding: 0.25rem 0.5rem;
        border-radius: 999px;
        font-size: 0.8rem;
    }
    
    .wiki-list {
        list-style: none;
        padding: 0;
        margin: 0;
    }
    
    .wiki-list li {
        padding: 0.5rem 0;
        border-bottom: 1px dashed var(--surface1);
    }
    
    .wiki-list li:last-child {
        border-bottom: none;
    }
    
    .wiki-list a {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        color: var(--text);
        text-decoration: none;
    }
    
    .wiki-list a:hover {
        color: var(--blue);
    }
    
    .wiki-list small {
        margin-left: auto;
        color: var(--subtext0);
        font-size: 0.8rem;
    }
    
    .empty {
        color: var(--subtext0);
        text-align: center;
        padding: 1rem 0;
    }
</style>
