% rebase('layout', title=page.title if page else "Create Page")
<link rel="stylesheet" href="/static/css/style.css">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/easymde/dist/easymde.min.css">
<script src="https://cdn.jsdelivr.net/npm/easymde/dist/easymde.min.js"></script>
<script src="/static/js/dark-mode.js"></script>

<div class="container">
    <nav class="breadcrumb mb-md">
        <a href="/wikis">Wikis</a> &raquo;
        <a href="/wikis/{{wiki.slug}}">{{wiki.name}}</a> &raquo;
        <span>{{page.title if page else "Create Page"}}</span>
    </nav>
    
    <div class="page-header">
        <div class="flex justify-between items-center">
            <h1 class="page-title">{{page.title if page else "Create New Page"}}</h1>
        </div>
    </div>
    
    <div class="content-body">
        <form method="POST" action="{{action_url}}" enctype="multipart/form-data" id="page-form">
            <div class="form-group">
                <label for="title">Page Title</label>
                <input type="text" class="form-control" id="title" name="title" 
                       value="{{page.title if page else ''}}" required>
            </div>
            
            <div class="form-group">
                <label for="slug">URL Slug</label>
                <input type="text" class="form-control" id="slug" name="slug" 
                       value="{{page.slug if page else ''}}" required>
                <small class="form-text text-muted">
                    Lowercase letters, numbers and hyphens only
                </small>
            </div>
            
            <div class="form-group">
                <label for="content">Content</label>
                <textarea class="form-control" id="content" name="content" rows="15" required>{{page.content if page else ''}}</textarea>
            </div>
            
            % if page: 
            <div class="form-group">
                <label for="comment">Edit Comment</label>
                <input type="text" class="form-control" id="comment" name="comment" 
                       placeholder="Briefly describe your changes">
            </div>
            % end
            
            <div class="form-actions mt-4">
                <button type="submit" class="btn btn-primary">
                    % if page:
                    <i class="fas fa-save"></i> Save Changes
                    % else:
                    <i class="fas fa-plus"></i> Create Page
                    % end
                </button>
                <a href="{{cancel_url}}" class="btn btn-secondary">Cancel</a>
            </div>
        </form>
    </div>
</div>

<script>
// Initialize EasyMDE
const easyMDE = new EasyMDE({
    element: document.getElementById('content'),
    autoDownloadFontAwesome: false,
    uploadImage: true,
    imageUploadEndpoint: '/wikis/{{wiki.slug}}/upload-media',
    imageCSRFToken: '{{get("csrf_token", "")}}',
    imagePathAbsolute: true,
    imageTexts: {
        sbInit: 'Drag and drop an image or click to browse',
        sbOnDragEnter: 'Drop your image here',
        sbOnDrop: 'Uploading...',
        sbProgress: 'Uploading... (#progress#)',
        sbOnUploaded: 'Uploaded!',
    },
    toolbar: [
        'bold', 'italic', 'heading', '|',
        'quote', 'unordered-list', 'ordered-list', '|',
        'link', 'image', '|',
        'preview', 'side-by-side', 'fullscreen', '|',
        'guide'
    ]
});

// Auto-slug generation
document.getElementById('title').addEventListener('blur', function() {
    const slugField = document.getElementById('slug');
    if (!slugField.value) {
        const slug = this.value.toLowerCase()
            .replace(/\s+/g, '-')    
            .replace(/[^\w-]+/g, '') 
            .replace(/-+/g, '-')   
            .replace(/^-+/, '')     
            .replace(/-+$/, '');    
        slugField.value = slug;
    }
});
</script>
