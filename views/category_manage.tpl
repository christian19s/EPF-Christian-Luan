% rebase('layout', title='Manage Categories')
<link rel="stylesheet" href="/static/css/style.css">

<div class="container">
    <div class="header">
        <h1><i class="fas fa-tags"></i> Manage Categories</h1>
        <a href="/categories/create" class="btn btn-primary">
            <i class="fas fa-plus"></i> New Category
        </a>
    </div>

    % if not categories:
        <div class="empty-state">
            <i class="fas fa-folder-open fa-2x"></i>
            <p>No categories created yet</p>
        </div>
    % else:
        <table class="table">
            <thead>
                <tr>
                    <th>Name</th>
                    <th>Slug</th>
                    <th>Color</th>
                    <th>Icon</th>
                    <th>Wikis</th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody>
                % for category in categories:
                <tr>
                    <td>
                        <i class="fas fa-{{category.icon}}" style="color: {{category.color}}"></i>
                        {{category.name}}
                    </td>
                    <td>{{category.slug}}</td>
                    <td>
                        <span class="color-preview" style="background: {{category.color}}"></span>
                        {{category.color}}
                    </td>
                    <td><code>{{category.icon}}</code></td>
                    <td>
                        {{category.wiki_count}} wiki{{'s' if category.wiki_count != 1 else ''}}
                    </td>
                    <td class="actions">
                        <a href="/categories/{{category.id}}/edit" class="btn btn-sm">
                            <i class="fas fa-edit"></i> Edit
                        </a>
                        <form method="POST" action="/categories/{{category.id}}/delete" style="display: inline;">
                            <button type="submit" class="btn btn-sm btn-danger" 
                                    onclick="return confirm('Delete this category? Wikis will become uncategorized.')">
                                <i class="fas fa-trash"></i> Delete
                            </button>
                        </form>
                    </td>
                </tr>
                % end
            </tbody>
        </table>
    % end
</div>

<style>
    .table {
        width: 100%;
        border-collapse: collapse;
        margin-top: 1rem;
    }
    
    .table th, .table td {
        padding: 0.75rem;
        border-bottom: 1px solid var(--surface1);
        text-align: left;
    }
    
    .table th {
        background: var(--surface0);
        font-weight: 600;
    }
    
    .color-preview {
        display: inline-block;
        width: 16px;
        height: 16px;
        border-radius: 3px;
        border: 1px solid var(--surface2);
        vertical-align: middle;
        margin-right: 0.5rem;
    }
    
    .actions {
        white-space: nowrap;
    }
    
    .actions form {
        display: inline-block;
        margin-left: 0.5rem;
    }
    
    code {
        background: var(--surface1);
        padding: 0.2rem 0.4rem;
        border-radius: 3px;
        font-family: monospace;
    }
    
    .empty-state {
        text-align: center;
        padding: 2rem;
        color: var(--text2);
    }
    
    .empty-state i {
        margin-bottom: 1rem;
    }
    
    .header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1.5rem;
    }
</style>
