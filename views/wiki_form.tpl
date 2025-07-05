% try:
    % hx_mode = hx_mode
% except:
    % hx_mode = False
% end

% if not hx_mode:
    % rebase('layout', title=('Edit Wiki' if wiki else 'Create New Wiki'))
    <link rel="stylesheet" href="/static/css/theme.css">
% end

% if not hx_mode:
    <div class="container">
% end

    <h1>{{ 'Edit Wiki' if wiki else 'Create New Wiki' }}</h1>
    
    % if get('error'):
        <div class="alert alert-error">{{error}}</div>
    % end
    
    <form method="POST" action="{{ action_url }}"
        % if hx_mode:
            hx-post="{{ action_url }}"
            hx-target="#create-wiki-modal"
            hx-swap="innerHTML"
        % end
    >
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
        
        <div class="form-footer">
            <button type="submit" class="btn btn-primary">
                {{ 'Update Wiki' if wiki else 'Create Wiki' }}
            </button>
            % if hx_mode:
                <button type="button" class="btn" 
                    _="on click remove .show from #create-wiki-modal then wait 200ms then set #create-wiki-modal's innerHTML to ''">
                    Cancel
                </button>
            % else:
                <a href="{{ cancel_url }}" class="btn">Cancel</a>
            % end
        </div>
    </form>

% if not hx_mode:
    </div>
% end

% if hx_mode:
    <script>
        // Auto-slugify the title
        document.getElementById('name').addEventListener('input', function(e) {
            const slugInput = document.getElementById('slug');
            if (!slugInput.value || slugInput.value === '') {
                slugInput.value = e.target.value
                    .toLowerCase()
                    .replace(/[^a-z0-9]+/g, '-')
                    .replace(/^-|-$/g, '');
            }
        });
    </script>
% end
