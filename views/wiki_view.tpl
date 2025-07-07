% rebase('layout', title='Todas as Wikis')
% categories = get('categories',[])
% user = get('user',None)
% error = get('error',None)
<link rel="stylesheet" href="/static/css/style.css">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">

<div class="container">
    <div class="wiki-header">
        <h1><i class="fas fa-sitemap"></i> Diretório de Wikis</h1>
        <div class="header-actions">
            % if user and user.can(PermissionSystem.CREATE_WIKI):
                <a href="/wikis/create" class="btn btn-sm btn-primary">
                    <i class="fas fa-plus"></i> Nova Wiki
                </a>
            % end
            % if user and user.can(PermissionSystem.MANAGE_CATEGORIES):
                <a href="/categories/manage" class="btn btn-sm btn-secondary">
                    <i class="fas fa-tags"></i> Gerenciar Categorias
                </a>
            % end

        </div>
    </div>

    % if error:
        <div class="alert alert-error">{{error}}</div>
    % end

    % if not categories:
        <div class="empty-state">
            <i class="fas fa-folder-open fa-2x"></i>
            <p>Nenhuma wiki criada ainda</p>
            % if user and user.can(PermissionSystem.CREATE_PAGE):
                <a href="/wikis/create" class="btn btn-primary">
                    <i class="fas fa-plus"></i> Criar Primeira Wiki
                </a>
            % end
        </div>
    % else:
        <div class="directory-tree">
            <ul class="tree">
                % for category in categories:
                <li class="tree-node category-node">
                    <div class="tree-item">
                        <span class="tree-caret"><i class="fas fa-caret-right"></i></span>
                        <span class="tree-icon"><i class="fas fa-{{category['icon']}}" style="color: {{category['color']}}"></i></span>
                        <span class="tree-label">{{category['name']}}</span>
                        <span class="tree-meta">{{len(category['wikis'])}} wiki{{'s' if len(category['wikis']) != 1 else ''}}</span>
                        % if user and user.can(PermissionSystem.MANAGE_CATEGORIES):
                        <div class="tree-actions">
                            <a href="/categories/{{category['id']}}/edit" title="Edit Category">
                                <i class="fas fa-edit"></i>
                            </a>
                        </div>
                        % end
                    </div>
                    
                    % if category['wikis']:
                    <ul class="tree-nested">
                        % for wiki in category['wikis']:
                        <li class="tree-node">
                            <div class="tree-item">
                                <span class="tree-caret"><i class="fas fa-caret-right"></i></span>
                                <span class="tree-icon"><i class="fas fa-book"></i></span>
                                <a href="/wikis/{{wiki['slug']}}" class="tree-label">{{wiki['name']}}</a>
                                <span class="tree-meta">{{wiki['created_at'][:10]}}</span>
                                % if user and (user.id == wiki['owner_id'] or user.can(PermissionSystem.MANAGE_WIKI, wiki['id'])):
                                <div class="tree-actions">
                                    <a href="/wikis/{{wiki['slug']}}/edit" title="Edit">
                                        <i class="fas fa-edit"></i>
                                    </a>
                                    <a href="/wikis/{{wiki['slug']}}/delete" title="Delete"
                                        onclick="return confirm('Deletar esta wiki permanentemente?')">
                                        <i class="fas fa-trash"></i>
                                    </a>
                                </div>
                                % end
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
/* Catppuccin Mocha color palette */
:root {
  --base: #1e1e2e;
  --mantle: #181825;
  --crust: #11111b;
  --text: #cdd6f4;
  --subtext0: #a6adc8;
  --subtext1: #bac2de;
  --surface0: #313244;
  --surface1: #45475a;
  --surface2: #585b70;
  --overlay0: #6c7086;
  --overlay1: #7f849c;
  --blue: #89b4fa;
  --red: #f38ba8;
  --green: #a6e3a1;
  --yellow: #f9e2af;
  --peach: #fab387;
  --mauve: #cba6f7;
  --pink: #f5c2e7;
  --teal: #94e2d5;
}

/* Base styles */
body {
  background-color: var(--base);
  color: var(--text);
  font-family: 'Segoe UI', system-ui, sans-serif;
  line-height: 1.6;
}

.container {
  max-width: 900px;
  margin: 0 auto;
  padding: 2rem 1rem;
}

/* Header styles */
.wiki-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid var(--surface0);
}

.wiki-header h1 {
  margin: 0;
  font-size: 1.8rem;
  color: var(--subtext1);
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.header-actions {
  display: flex;
  gap: 0.75rem;
  align-items: center;
}

/* Button styles */
.btn {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  font-weight: 500;
  transition: all 0.2s ease;
  border: none;
  cursor: pointer;
  text-decoration: none;
}

.btn-sm {
  padding: 0.4rem 0.8rem;
  font-size: 0.9rem;
}

.btn-primary {
  background-color: var(--mauve);
  color: var(--crust);
}

.btn-primary:hover {
  background-color: var(--pink);
}

.btn-secondary {
  background-color: var(--surface0);
  color: var(--text);
}

.btn-secondary:hover {
  background-color: var(--surface1);
}

.btn i {
  font-size: 0.9em;
}

/* Alert styles */
.alert {
  padding: 1rem;
  border-radius: 8px;
  margin-bottom: 1.5rem;
}

.alert-error {
  background-color: rgba(243, 139, 168, 0.15);
  border: 1px solid var(--red);
  color: var(--red);
}

/* Empty state */
.empty-state {
  text-align: center;
  padding: 3rem 2rem;
  background-color: var(--mantle);
  border-radius: 12px;
  border: 1px dashed var(--surface0);
}

.empty-state i {
  margin-bottom: 1rem;
  color: var(--overlay0);
}

.empty-state p {
  color: var(--subtext0);
  margin-bottom: 1.5rem;
}

/* Tree structure */
.directory-tree {
  background-color: var(--mantle);
  border-radius: 12px;
  padding: 1.5rem;
  border: 1px solid var(--surface0);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.tree {
  list-style-type: none;
  padding-left: 0;
  margin: 0;
}

.tree-node {
  margin-bottom: 0.25rem;
}

.tree-item {
  display: flex;
  align-items: center;
  padding: 0.6rem 1rem;
  border-radius: 8px;
  transition: all 0.2s ease;
  position: relative;
}

.tree-item:hover {
  background-color: var(--surface0);
}

.tree-caret {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 24px;
  height: 24px;
  cursor: pointer;
  margin-right: 0.5rem;
  transition: transform 0.2s ease;
  color: var(--overlay0);
}

.tree-caret.caret-down {
  transform: rotate(90deg);
}

.tree-caret i {
  font-size: 0.9rem;
}

.tree-icon {
  width: 24px;
  height: 24px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  margin-right: 0.75rem;
  color: var(--blue);
}

.tree-label {
  flex: 1;
  color: var(--subtext1);
  font-weight: 500;
}

.tree-label a {
  color: var(--subtext1);
  text-decoration: none;
  transition: color 0.2s ease;
}

.tree-label a:hover {
  color: var(--blue);
  text-decoration: underline;
}

.tree-meta {
  color: var(--overlay0);
  font-size: 0.85rem;
  margin-left: 1rem;
  font-family: 'Fira Code', monospace;
}

.tree-actions {
  display: flex;
  gap: 0.75rem;
  margin-left: 1rem;
  opacity: 0;
  transition: opacity 0.2s ease;
}

.tree-item:hover .tree-actions {
  opacity: 1;
}

.tree-actions a {
  color: var(--overlay0);
  transition: color 0.2s ease;
  text-decoration: none;
}

.tree-actions a:hover {
  color: var(--blue);
}

.tree-actions a.delete:hover {
  color: var(--red);
}

.tree-nested {
  list-style-type: none;
  padding-left: 2.5rem;
  margin-top: 0.25rem;
  border-left: 1px solid var(--surface0);
  display: none;
}

.tree-nested.active {
  display: block;
}

/* Category node styling */
.category-node .tree-icon {
  color: var(--peach);
}

.category-node .tree-label {
  color: var(--peach);
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .wiki-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }
  
  .header-actions {
    width: 100%;
    justify-content: space-between;
  }
  
  .tree-meta {
    display: none;
  }
  
  .tree-actions {
    opacity: 1;
  }
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

    // Auto-expand categories with active wikis
    document.querySelectorAll('.category-node .tree-item').forEach(item => {
        const nested = item.nextElementSibling;
        if (nested && nested.querySelector('.tree-node')) {
            item.querySelector('.tree-caret').classList.add('caret-down');
            nested.classList.add('active');
        }
    });
});
</script>

<script src="/static/js/dark-mode.js"></script>
