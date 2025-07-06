% rebase('layout', title=('Edit Wiki' if wiki else 'Create New Wiki'))
<link rel="stylesheet" href="/static/css/style.css">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">

<div class="wiki-form-container">
    <div class="wiki-form-header">
        <h1><i class="fas fa-book"></i> {{ 'Edit Wiki' if wiki else 'Create New Wiki' }}</h1>
        <div class="form-actions">
            <a href="{{ cancel_url }}" class="btn btn-secondary">
                <i class="fas fa-times"></i> Cancel
            </a>
            <button type="submit" form="wiki-form" class="btn btn-primary">
                <i class="fas fa-save"></i> {{ 'Update' if wiki else 'Create' }}
            </button>
        </div>
    </div>

    % if get('errors'):
        <div class="form-alert">
            <i class="fas fa-exclamation-circle"></i>
            <div class="alert-content">
                % for error in errors:
                    <p>{{error}}</p>
                % end
            </div>
        </div>
    % end

    <form id="wiki-form" method="POST" action="{{ action_url }}">
        <div class="form-section">
            <h2><i class="fas fa-info-circle"></i> Basic Information</h2>
            
            <div class="form-group">
                <label for="name">Wiki Name</label>
                <input type="text" id="name" name="name" 
                       value="{{ wiki.name if wiki else '' }}" 
                       placeholder="Enter wiki name" required>
            </div>

            <div class="form-group">
                <label for="slug">URL Slug</label>
                <div class="input-group">
                    <span class="input-prefix">/wikis/</span>
                    <input type="text" id="slug" name="slug" 
                           value="{{ wiki.slug if wiki else '' }}" 
                           placeholder="wiki-slug" required>
                </div>
                <small>Lowercase letters, numbers, and hyphens only</small>
            </div>

            <div class="form-group">
                <label for="description">Description</label>
                <textarea id="description" name="description" rows="3" 
                          placeholder="Brief description of this wiki">{{ wiki.description if wiki else '' }}</textarea>
            </div>
        </div>
        
        <div class="form-section">
            <h2><i class="fas fa-folder-tree"></i> Organization</h2>
            
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
        </div>
    </form>
</div>

<style>
.wiki-form-container {
    max-width: 780px;
    margin: 2rem auto;
    background: var(--mantle);
    border-radius: 12px;
    border: 1px solid var(--surface0);
    box-shadow: 0 5px 20px rgba(0, 0, 0, 0.1);
    overflow: hidden;
}

.wiki-form-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1.5rem;
    background: var(--surface0);
    border-bottom: 1px solid var(--surface1);
}

.wiki-form-header h1 {
    margin: 0;
    font-size: 1.5rem;
    display: flex;
    align-items: center;
    gap: 12px;
    color: var(--subtext1);
}

.form-actions {
    display: flex;
    gap: 0.75rem;
}

.form-section {
    padding: 1.5rem;
    border-bottom: 1px solid var(--surface1);
}

.form-section:last-child {
    border-bottom: none;
}

.form-section h2 {
    margin-top: 0;
    margin-bottom: 1.5rem;
    font-size: 1.2rem;
    color: var(--subtext1);
    display: flex;
    align-items: center;
    gap: 10px;
}

.form-group {
    margin-bottom: 1.5rem;
}

label {
    display: block;
    margin-bottom: 0.5rem;
    font-weight: 500;
    color: var(--subtext0);
}

input[type="text"],
textarea,
select {
    width: 100%;
    padding: 0.75rem;
    border: 1px solid var(--surface1);
    border-radius: 6px;
    background: var(--base);
    color: var(--text);
    font-family: inherit;
}

input[type="text"]:focus,
textarea:focus,
select:focus {
    outline: none;
    border-color: var(--blue);
    box-shadow: 0 0 0 2px rgba(137, 180, 250, 0.2);
}

textarea {
    min-height: 120px;
    resize: vertical;
    line-height: 1.5;
}

small {
    display: block;
    margin-top: 0.25rem;
    font-size: 0.85rem;
    color: var(--subtext0);
}

.form-alert {
    display: flex;
    gap: 1rem;
    padding: 1.25rem;
    background: rgba(243, 139, 168, 0.1);
    border-left: 4px solid var(--red);
    color: var(--red);
    align-items: flex-start;
}

.form-alert i {
    font-size: 1.2rem;
    margin-top: 2px;
}

.alert-content p {
    margin: 0.5rem 0;
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

/* Input group */
.input-group {
    display: flex;
}

.input-prefix {
    padding: 0.75rem;
    background: var(--surface1);
    border: 1px solid var(--surface1);
    border-right: none;
    border-radius: 6px 0 0 6px;
    color: var(--subtext0);
    font-size: 0.9rem;
}

.input-group input {
    border-radius: 0 6px 6px 0;
    flex: 1;
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

// Initialize theme manager
document.addEventListener('DOMContentLoaded', ThemeManager.init);
</script>
