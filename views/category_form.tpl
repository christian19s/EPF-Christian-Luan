% rebase('layout', title=('Edit Category' if category else 'Create Category'))
<link rel="stylesheet" href="/static/css/style.css">

<div class="container">
    <div class="header">
        <h1>{{ 'Edit Category' if category else 'Create New Category' }}</h1>
        <a href="/categories/manage" class="btn">
            <i class="fas fa-arrow-left"></i> Back to Categories
        </a>
    </div>

    % if get('errors'):
        <div class="alert alert-error">
            % for error in errors:
                <p>{{error}}</p>
            % end
        </div>
    % end

    <form method="POST" action="{{ request.path }}">
        <div class="form-group">
            <label for="name">Category Name</label>
            <input type="text" id="name" name="name" 
                   value="{{ category.name if category else '' }}" 
                   required>
        </div>

        <div class="form-group">
            <label for="slug">URL Slug</label>
            <input type="text" id="slug" name="slug" 
                   value="{{ category.slug if category else '' }}" 
                   required>
            <small>Lowercase letters, numbers, and hyphens only</small>
        </div>

        <div class="form-group">
            <label for="description">Description</label>
            <textarea id="description" name="description" rows="3">{{ category.description if category else '' }}</textarea>
        </div>

        <div class="form-row">
            <div class="form-group">
                <label for="color">Color</label>
                <div class="color-picker">
                    <input type="color" id="color" name="color" 
                           value="{{ category.color if category else '#6b7280' }}">
                    <input type="text" id="color-text" 
                           value="{{ category.color if category else '#6b7280' }}"
                           pattern="^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$">
                </div>
            </div>

            <div class="form-group">
                <label for="icon">Icon</label>
                <select id="icon" name="icon" required>
                    % icons = ['folder', 'book', 'tag', 'hashtag', 'star', 'database', 'globe', 'code', 'image', 'file', 'archive', 'box']
                    % for icon_choice in icons:
                        <option value="{{icon_choice}}" 
                                {{ 'selected' if category and category.icon == icon_choice else '' }}>
                            <i class="fas fa-{{icon_choice}}"></i> {{icon_choice}}
                        </option>
                    % end
                </select>
            </div>
        </div>

        <div class="form-footer">
            <button type="submit" class="btn btn-primary">
                {{ 'Update Category' if category else 'Create Category' }}
            </button>
            <a href="/categories/manage" class="btn">Cancel</a>
        </div>
    </form>
</div>

<style>
    .alert-error {
        background: var(--surface1);
        border-left: 4px solid var(--red);
        padding: 1rem;
        margin-bottom: 1.5rem;
    }
    
    .form-row {
        display: flex;
        gap: 1rem;
    }
    
    .form-row .form-group {
        flex: 1;
    }
    
    .color-picker {
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .color-picker input[type="color"] {
        width: 50px;
        height: 40px;
        padding: 2px;
        background: var(--surface1);
        border-radius: 4px;
        cursor: pointer;
    }
    
    .color-picker input[type="text"] {
        flex: 1;
        font-family: monospace;
    }
    
    select option {
        padding: 0.5rem;
    }
    
    .form-error {
        color: var(--red);
        font-size: 0.9rem;
        margin-top: 0.25rem;
    }
</style>

<script>
    // Sync color inputs
    document.getElementById('color').addEventListener('input', function(e) {
        document.getElementById('color-text').value = e.target.value;
    });
    
    document.getElementById('color-text').addEventListener('input', function(e) {
        if (/^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$/.test(e.target.value)) {
            document.getElementById('color').value = e.target.value;
        }
    });
    
    // Auto-generate slug from name
    document.getElementById('name').addEventListener('input', function(e) {
        if (!document.getElementById('slug').value) {
            const slug = e.target.value
                .toLowerCase()
                .replace(/[^a-z0-9]+/g, '-')
                .replace(/^-|-$/g, '');
            document.getElementById('slug').value = slug;
        }
    });
</script>
