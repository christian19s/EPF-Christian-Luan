% rebase('layout', title=('Edit Wiki' if wiki else 'Create New Wiki'))
<link rel="stylesheet" href="/static/css/style.css">

<div class="container">
    <div class="header">
        <h1>{{ 'Edit Wiki' if wiki else 'Create New Wiki' }}</h1>
        <a href="{{ cancel_url }}" class="btn">
            <i class="fas fa-arrow-left"></i> Cancel
        </a>
    </div>

    % if get('errors'):
        <div class="alert alert-error">
            % for error in errors:
                <p>{{error}}</p>
            % end
        </div>
    % end

    <form method="POST" action="{{ action_url }}">
        <div class="form-group">
            <label for="name">Wiki Name</label>
            <input type="text" id="name" name="name" 
                   value="{{ wiki.name if wiki else '' }}" 
                   required>
        </div>

        <div class="form-group">
            <label for="slug">URL Slug</label>
            <input type="text" id="slug" name="slug" 
                   value="{{ wiki.slug if wiki else '' }}" 
                   required>
            <small>Lowercase letters, numbers, and hyphens only</small>
        </div>

        <div class="form-group">
            <label for="description">Description</label>
            <textarea id="description" name="description" rows="3">{{ wiki.description if wiki else '' }}</textarea>
        </div>
        
        <div class="form-group">
            <label for="category_id">Category</label>
            <select id="category_id" name="category_id">
                <option value="">-- No Category --</option>
                % for category in categories:
                    <option value="{{category['id']}}" 
                        {{ 'selected' if wiki and wiki.category_id == category['id'] else '' }}>
                        {{category['name']}}
                    </option>
                % end
            </select>
        </div>

        <div class="form-footer">
            <button type="submit" class="btn btn-primary">
                {{ 'Update Wiki' if wiki else 'Create Wiki' }}
            </button>
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
    
    .form-footer {
        display: flex;
        justify-content: flex-end;
        gap: 0.5rem;
        margin-top: 1rem;
    }
</style>

<script>
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
