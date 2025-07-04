% rebase('layout', title=('Edit Wiki' if wiki else 'Create New Wiki'))
<link rel="stylesheet" href="/static/css/style.css">

<div class="container">
    <h1>{{ 'Edit Wiki' if wiki else 'Create New Wiki' }}</h1>
    
    % if get('error'):
        <div class="alert alert-error">{{error}}</div>
    % end
    
    <form method="POST" action="{{ action_url }}">
        <div class="form-group">
            <label class="form-label" for="name">Wiki Name</label>
            <input type="text" id="name" name="name" class="form-control" 
                   value="{{ wiki.name if wiki else '' }}" required>
        </div>
        
        <div class="form-group">
            <label class="form-label" for="slug">URL Slug</label>
            <input type="text" id="slug" name="slug" class="form-control" 
                   value="{{ wiki.slug if wiki else '' }}" required>
            <small class="text-muted">This will be part of the URL (e.g., /wikis/your-slug)</small>
        </div>
        
        <div class="form-group">
            <label class="form-label" for="description">Description (Optional)</label>
            <textarea id="description" name="description" class="form-control" 
                      rows="3">{{ wiki.description if wiki else '' }}</textarea>
        </div>
        
        <button type="submit" class="btn btn-primary">
            {{ 'Update Wiki' if wiki else 'Create Wiki' }}
        </button>
        <a href="{{ cancel_url }}" class="btn">Cancel</a>
    </form>
</div>
