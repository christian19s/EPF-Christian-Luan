% rebase('layout', title='All Wikis')
<link rel="stylesheet" href="/static/css/style.css">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">

<div class="container">
    <div class="wiki-header">
        <h1><i class="fas fa-sitemap"></i> Wiki Directory</h1>
        <div class="header-actions">
            % if user and user.can(PermissionSystem.CREATE_WIKI):
                <a href="/wikis/create" class="btn btn-sm btn-primary">
                    <i class="fas fa-plus"></i> New Wiki
                </a>
            % end
            <button id="themeToggle" class="btn btn-sm">
                <i class="fas fa-moon"></i>
                <span id="themeText">Dark Mode</span>
            </button>
        </div>
    </div>

    % if get('error'):
        <div class="alert alert-error">{{error}}</div>
    % end

    % if not wikis:
        <div class="empty-state">
            <i class="fas fa-folder-open fa-2x"></i>
            <p>No wikis created yet</p>
            % if user and user.can(PermissionSystem.CREATE_PAGE):
                <a href="/wikis/create" class="btn btn-primary">
                    <i class="fas fa-plus"></i> Create First Wiki
                </a>
            % end
        </div>
    % else:
        <div class="directory-tree">
            <ul class="tree">
                % for wiki in wikis:
                <li class="tree-node">
                    <div class="tree-item">
                        <span class="tree-caret"><i class="fas fa-caret-right"></i></span>
                        <span class="tree-icon"><i class="fas fa-book"></i></span>
                        <a href="/wikis/{{wiki.slug}}" class="tree-label">{{wiki.name}}</a>
                        <span class="tree-meta">{{wiki.created_at[:10]}}</span>
                        % if user and (user.id == wiki.owner_id or user.can(PermissionSystem.MANAGE_WIKI, wiki.id)):
                        <div class="tree-actions">
                            <a href="/wikis/{{wiki.slug}}/edit" title="Edit">
                                <i class="fas fa-edit"></i>
                            </a>
                            <a href="/wikis/{{wiki.slug}}/delete" title="Delete"
                                onclick="return confirm('Delete this wiki permanently?')">
                                <i class="fas fa-trash"></i>
                            </a>
                        </div>
                        % end
                    </div>
                    % if hasattr(wiki, 'pages') and wiki.pages:
                    <ul class="tree-nested">
                        % for page in wiki.pages:
                        <li class="tree-node">
                            <div class="tree-item">
                                <span class="tree-icon"><i class="fas fa-file-alt"></i></span>
                                <a href="/wikis/{{wiki.slug}}/{{page.slug}}" class="tree-label">{{page.title}}</a>
                                <span class="tree-meta">{{page.created_at[:10]}}</span>
                            </div>
                        </li>
                        % end
                    </ul>
                    % end
                </li>
                % end
            </ul>
        </div>
    % end
</div>

<style>
    :root {
        /* Light theme defaults */
        --base: #fbf1c7;
        --mantle: #f2e5bc;
        --crust: #ebdbb2;
        --surface0: #d5c4a1;
        --surface1: #bdae93;
        --surface2: #a89984;
        --text: #3c3836;
        --subtext0: #665c54;
        --subtext1: #7c6f64;
        --blue: #458588;
        
        /* Tree specific */
        --tree-line: #bdae93;
        --tree-icon: #665c54;
        --tree-hover: #f2e5bc;
    }

    .dark-mode {
        --base: #1e1e2e;
        --mantle: #181825;
        --crust: #11111b;
        --surface0: #313244;
        --surface1: #45475a;
        --surface2: #585b70;
        --text: #cdd6f4;
        --subtext0: #a6adc8;
        --subtext1: #bac2de;
        --blue: #89b4fa;
        
        --tree-line: #585b70;
        --tree-icon: #a6adc8;
        --tree-hover: #45475a;
    }

    body {
        background: var(--base);
        color: var(--text);
        transition: background 0.3s, color 0.3s;
    }

    .wiki-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1.5rem;
        padding-bottom: 1rem;
        border-bottom: 1px solid var(--surface1);
    }

    .header-actions {
        display: flex;
        gap: 0.5rem;
        align-items: center;
    }

    .directory-tree {
        background: var(--base);
        border-radius: 8px;
        padding: 1rem;
    }

    .tree {
        list-style-type: none;
        padding-left: 0;
    }

    .tree-node {
        position: relative;
        padding-left: 1.5rem;
        margin: 0.25rem 0;
    }

    .tree-node:before {
        content: "";
        position: absolute;
        top: 0;
        left: 10px;
        height: 100%;
        border-left: 1px dashed var(--tree-line);
    }

    .tree-node:last-child:before {
        height: 1.2rem;
    }

    .tree-item {
        display: flex;
        align-items: center;
        padding: 0.3rem 0.5rem;
        border-radius: 4px;
        transition: background 0.2s;
    }

    .tree-item:hover {
        background: var(--tree-hover);
    }

    .tree-caret {
        margin-right: 0.5rem;
        cursor: pointer;
        transition: transform 0.2s;
        color: var(--tree-icon);
    }

    .tree-caret i {
        width: 1rem;
        text-align: center;
    }

    .tree-caret.caret-down i {
        transform: rotate(90deg);
    }

    .tree-icon {
        margin-right: 0.5rem;
        color: var(--tree-icon);
        width: 1rem;
        text-align: center;
    }

    .tree-label {
        flex: 1;
        color: var(--text);
        text-decoration: none;
    }

    .tree-label:hover {
        color: var(--blue);
    }

    .tree-meta {
        font-size: 0.8rem;
        color: var(--subtext0);
        margin-left: 1rem;
    }

    .tree-actions {
        display: flex;
        gap: 0.8rem;
        margin-left: 1rem;
    }

    .tree-actions a {
        color: var(--subtext0);
        transition: color 0.2s;
    }

    .tree-actions a:hover {
        color: var(--blue);
    }

    .tree-nested {
        display: none;
        list-style-type: none;
        padding-left: 1.5rem;
    }

    .tree-nested.active {
        display: block;
    }

    /* Button styles */
    .btn {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.5rem 1rem;
        border-radius: 4px;
        background: var(--surface1);
        color: var(--text);
        border: none;
        cursor: pointer;
        text-decoration: none;
        transition: background 0.2s;
    }

    .btn:hover {
        background: var(--surface2);
    }

    .btn-sm {
        padding: 0.3rem 0.7rem;
        font-size: 0.9rem;
    }

    .btn-primary {
        background: var(--blue);
        color: white;
    }

    .empty-state {
        text-align: center;
        padding: 2rem;
        color: var(--subtext0);
    }

    .empty-state i {
        margin-bottom: 1rem;
        color: var(--subtext0);
    }

    .alert-error {
        padding: 1rem;
        background: var(--red);
        color: white;
        border-radius: 4px;
        margin-bottom: 1rem;
    }
</style>

<script>
document.addEventListener('DOMContentLoaded', function() {
    // Initialize dark mode
    ThemeManager.init();
    
    // Tree functionality
    const carets = document.querySelectorAll('.tree-caret');
    carets.forEach(caret => {
        caret.addEventListener('click', function() {
            this.classList.toggle('caret-down');
            const nested = this.parentElement.nextElementSibling;
            if (nested) {
                nested.classList.toggle('active');
            }
        });
    });
});
</script>

<script src="/static/js/dark-mode.js"></script>
