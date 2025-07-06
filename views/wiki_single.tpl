% rebase('layout', title=wiki.name)
<link rel="stylesheet" href="/static/css/style.css">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">

<div class="wiki-container">
    <div class="wiki-header">
        <h1><i class="fas fa-book"></i> {{wiki.name}}</h1>
        <p class="wiki-description">{{wiki.description}}</p>
        <div class="wiki-meta">
            <span>Created by {{wiki.owner_username}} on {{wiki.created_at[:10]}}</span>
        </div>
        
        % if wiki.category_id:
        <div class="wiki-category">
            <i class="fas fa-folder"></i>
            <span>{{wiki.category_name}}</span>
        </div>
        % end
        
        % if user and (user.id == wiki.owner_id or user.can(PermissionSystem.MANAGE_WIKI, wiki.id)):
            <div class="wiki-actions">
                <a href="/wikis/{{wiki.slug}}/edit" class="btn btn-secondary">
                    <i class="fas fa-edit"></i> Edit Wiki
                </a>
                <a href="/wikis/{{wiki.slug}}/pages/create" class="btn btn-primary">
                    <i class="fas fa-plus"></i> New Page
                </a>
            </div>
        % end
    </div>

    % if not pages:
        <div class="empty-state">
            <i class="fas fa-file-alt fa-3x"></i>
            <h3>No pages created yet</h3>
            <p>Get started by creating your first page</p>
            % if user and user.can(PermissionSystem.CREATE_PAGE, wiki.id):
                <a href="/wikis/{{wiki.slug}}/pages/create" class="btn btn-primary">
                    Create First Page
                </a>
            % end
        </div>
    % else:
        <div class="page-grid">
            % for page in pages:
            <a href="/wikis/{{wiki.slug}}/{{page.slug}}" class="page-card">
                <div class="page-icon">
                    <i class="fas fa-file-alt"></i>
                </div>
                <div class="page-content">
                    <h3>{{page.title}}</h3>
                    <div class="page-meta">
                        <span>Created on {{page.created_at[:10]}}</span>
                    </div>
                </div>
            </a>
            % end
        </div>
    % end
</div>

<style>
.wiki-container {
    max-width: 800px;
    margin: 2rem auto;
    background: var(--mantle);
    border-radius: 12px;
    border: 1px solid var(--surface0);
    box-shadow: 0 5px 20px rgba(0, 0, 0, 0.1);
    overflow: hidden;
}

.wiki-header {
    padding: 2rem;
    background: var(--surface0);
    border-bottom: 1px solid var(--surface1);
}

.wiki-header h1 {
    margin-top: 0;
    display: flex;
    align-items: center;
    gap: 12px;
    color: var(--subtext1);
}

.wiki-description {
    font-size: 1.1rem;
    color: var(--text);
    margin: 1rem 0;
}

.wiki-meta {
    font-size: 0.9rem;
    color: var(--subtext0);
    margin-bottom: 0.5rem;
}

.wiki-category {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 0.9rem;
    color: var(--subtext0);
    margin-bottom: 1rem;
}

.wiki-actions {
    display: flex;
    gap: 0.75rem;
    margin-top: 1.5rem;
}

.empty-state {
    text-align: center;
    padding: 3rem 2rem;
    background: var(--base);
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

.page-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 1.5rem;
    padding: 2rem;
}

.page-card {
    display: flex;
    flex-direction: column;
    background: var(--base);
    border-radius: 8px;
    overflow: hidden;
    text-decoration: none;
    color: inherit;
    border: 1px solid var(--surface0);
    transition: transform 0.2s, box-shadow 0.2s;
}

.page-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
    border-color: var(--surface1);
}

.page-icon {
    background: linear-gradient(135deg, var(--blue), var(--teal));
    height: 120px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 2.5rem;
    color: white;
}

.page-content {
    padding: 1.5rem;
}

.page-content h3 {
    margin-top: 0;
    margin-bottom: 0.5rem;
    color: var(--subtext1);
}

.page-meta {
    font-size: 0.85rem;
    color: var(--subtext0);
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

.btn-secondary {
    background-color: transparent;
    color: var(--subtext0);
    border: 1px solid var(--surface1);
}

.btn-secondary:hover {
    background-color: var(--surface0);
    color: var(--text);
}
</style>

<script>
// Initialize theme manager
document.addEventListener('DOMContentLoaded', ThemeManager.init);
</script>
