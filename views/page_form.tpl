% rebase('layout', title=('Edit Page' if page else 'Create New Page'))
<link rel="stylesheet" href="/static/css/style.css">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/simplemde/latest/simplemde.min.css">
<script src="https://cdn.jsdelivr.net/simplemde/latest/simplemde.min.js"></script>

<div class="container">
    <nav class="breadcrumb mb-md">
        <a href="/wikis">Wikis</a> &raquo;
        <a href="/wikis/{{wiki.slug}}">{{wiki.name}}</a> &raquo;
        <span>{{ 'Edit Page' if page else 'Create Page' }}</span>
    </nav>
    
    <h1>{{ page.title if page else 'Create New Page' }}</h1>
    
    % if get('error'):
        <div class="alert alert-error">{{error}}</div>
    % end
    
    <form method="POST" action="{{ action_url }}">
        <div class="form-group">
            <label class="form-label" for="title">Page Title</label>
            <input type="text" id="title" name="title" class="form-control" 
                   value="{{ page.title if page else '' }}" required>
        </div>
        
        <div class="form-group">
            <label class="form-label" for="slug">URL Slug</label>
            <input type="text" id="slug" name="slug" class="form-control" 
                   value="{{ page.slug if page else '' }}" required>
        </div>
        
        <div class="form-group">
            <label class="form-label" for="content">Content</label>
            <textarea id="content" name="content" class="form-control" rows="15">{{ page.content if page else '' }}</textarea>
        </div>
        
        <div class="form-group">
            <label class="form-label" for="comment">Edit Summary (Optional)</label>
            <input type="text" id="comment" name="comment" class="form-control" 
                   placeholder="Briefly describe your changes">
        </div>
        
        <button type="submit" class="btn btn-primary">
            {{ 'Update Page' if page else 'Create Page' }}
        </button>
        <a href="{{ cancel_url }}" class="btn">Cancel</a>
    </form>
</div>

<script>
    // Initialize Markdown editor
    const simplemde = new SimpleMDE({ 
        element: document.getElementById("content"),
        spellChecker: false,
        toolbar: [
            "bold", "italic", "heading", "|",
            "quote", "unordered-list", "ordered-list", "|",
            "link", "image", "|",
            "preview", "guide"
        ]
    });
    
    // Auto-generate slug from title
    document.getElementById('title').addEventListener('input', function() {
        if (!document.getElementById('slug').value) {
            const slug = this.value
                .toLowerCase()
                .replace(/[^\w\s]/g, '')
                .replace(/\s+/g, '-');
            document.getElementById('slug').value = slug;
        }
    });
</script>
