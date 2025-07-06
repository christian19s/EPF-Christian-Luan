% rebase('layout', title=('Edit Category' if category else 'Create Category'))
<link rel="stylesheet" href="/static/css/style.css">

<div class="container">
    <div class="header">
        <h1>{{ 'Edit Category' if category else 'Create New Category' }}</h1>
        <a href="/categories/manage" class="btn">
            <i class="fas fa-arrow-left"></i> Back to Categories
        </a>
    </div>

    % if 'errors' in locals() and errors:
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
                   value="{{ category.name if hasattr(category, 'name') else (form_data['name'] if 'form_data' in locals() and 'name' in form_data else '') }}" 
                   required>
        </div>

        <div class="form-group">
            <label for="slug">URL Slug</label>
            <input type="text" id="slug" name="slug" 
                   value="{{ category.slug if hasattr(category, 'slug') else (form_data['slug'] if 'form_data' in locals() and 'slug' in form_data else '') }}" 
                   required>
            <small>Lowercase letters, numbers, and hyphens only</small>
        </div>

        <div class="form-group">
            <label for="description">Description</label>
            <textarea id="description" name="description" rows="3">{{ category.description if hasattr(category, 'description') else (form_data['description'] if 'form_data' in locals() and 'description' in form_data else '') }}</textarea>
        </div>

        <div class="form-row">
            <div class="form-group">
                <label for="color">Color</label>
                <div class="color-picker">
                    <input type="color" id="color" name="color" 
                           value="{{ category.color if hasattr(category, 'color') else (form_data['color'] if 'form_data' in locals() and 'color' in form_data else '#6b7280') }}">
                    <input type="text" id="color-text" 
                           value="{{ category.color if hasattr(category, 'color') else (form_data['color'] if 'form_data' in locals() and 'color' in form_data else '#6b7280') }}"
                           pattern="^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$">
                </div>
            </div>

            <div class="form-group">
                <label for="icon">Icon</label>
                <select id="icon" name="icon" required>
                    % icons = ['folder', 'book', 'tag', 'hashtag', 'star', 'database', 'globe', 'code', 'image', 'file', 'archive', 'box']
                    % current_icon = category.icon if hasattr(category, 'icon') else (form_data['icon'] if 'form_data' in locals() and 'icon' in form_data else 'folder')
                    % for icon_choice in icons:
                        <option value="{{icon_choice}}" 
                                {{ 'selected' if icon_choice == current_icon else '' }}>
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
    .container {
        max-width: 800px;
        margin: 0 auto;
        padding: 2rem;
    }
    
    .header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 2rem;
    }
    
    .btn {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.5rem 1rem;
        background: var(--surface1);
        border: 1px solid var(--surface3);
        border-radius: 4px;
        text-decoration: none;
        color: var(--text1);
        cursor: pointer;
    }
    
    .btn-primary {
        background: var(--brand);
        color: white;
        border-color: var(--brand);
    }
    
    .btn-primary:hover {
        background: var(--brand-hover);
    }
    
    .form-group {
        margin-bottom: 1.5rem;
    }
    
    label {
        display: block;
        margin-bottom: 0.5rem;
        font-weight: 500;
    }
    
    input[type="text"],
    textarea,
    select {
        width: 100%;
        padding: 0.5rem;
        border: 1px solid var(--surface3);
        border-radius: 4px;
        background: var(--surface1);
        color: var(--text1);
    }
    
    textarea {
        min-height: 100px;
        resize: vertical;
    }
    
    small {
        display: block;
        margin-top: 0.25rem;
        font-size: 0.8rem;
        color: var(--text2);
    }
    
    .alert-error {
        background: var(--surface1);
        border-left: 4px solid var(--red);
        padding: 1rem;
        margin-bottom: 1.5rem;
    }
    
    .alert-error p {
        margin: 0;
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
    
    .form-footer {
        display: flex;
        justify-content: flex-end;
        gap: 0.5rem;
        margin-top: 1rem;
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
