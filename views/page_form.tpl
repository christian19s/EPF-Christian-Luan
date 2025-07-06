% rebase('layout', title=page.title if page else "Create Page")
<link rel="stylesheet" href="/static/css/style.css">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.7.0/styles/github.min.css">
<script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.7.0/highlight.min.js"></script>
<script src="https://unpkg.com/htmx.org@1.9.4"></script>
<script>hljs.highlightAll();</script>
<script src="/static/js/dark-mode.js"></script>

<style>
  .editor-container {
    border: 1px solid var(--border-color);
    border-radius: 6px;
    overflow: hidden;
    margin-bottom: 1.5rem;
  }
  
  .media-upload-section {
    background: var(--surface-2);
    padding: 1rem;
    border-radius: 6px;
    margin-top: 1.5rem;
  }
  
  .media-preview {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(100px, 1fr));
    gap: 1rem;
    margin-top: 1rem;
  }
  
  .media-preview-item {
    position: relative;
    border-radius: 4px;
    overflow: hidden;
    background: var(--surface-3);
  }
  
  .media-preview-item img {
    width: 100%;
    height: 80px;
    object-fit: cover;
  }
  
  .remove-media {
    position: absolute;
    top: 2px;
    right: 2px;
    background: rgba(0,0,0,0.5);
    color: white;
    border: none;
    border-radius: 50%;
    width: 20px;
    height: 20px;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 10px;
  }
  
  .editor-toolbar {
    background: var(--surface-2);
    padding: 0.5rem;
    border-bottom: 1px solid var(--border-color);
  }
  
  .editor-toolbar button {
    background: var(--surface-3);
    border: none;
    border-radius: 4px;
    padding: 0.25rem 0.5rem;
    margin-right: 0.25rem;
    cursor: pointer;
  }
</style>

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
                <label for="content">Content (Markdown)</label>
                <div class="editor-container">
                    <div class="editor-toolbar">
                        <button type="button" data-command="bold"><strong>B</strong></button>
                        <button type="button" data-command="italic"><em>I</em></button>
                        <button type="button" data-command="heading">H</button>
                        <button type="button" data-command="link">🔗</button>
                        <button type="button" data-command="image">🖼️</button>
                        <button type="button" data-command="code">&lt;&gt;</button>
                        <button type="button" data-command="unordered-list">• List</button>
                    </div>
                    <textarea class="form-control" id="content" name="content" 
                              rows="15" required>{{page.content if page else ''}}</textarea>
                </div>
            </div>
            
            <div class="media-upload-section">
                <h4>Attach Media</h4>
                <div class="flex items-center">
                    <input type="file" id="media-file" name="media" accept="image/*,video/*,application/pdf">
                    <button type="button" class="btn btn-secondary ml-2"
                            hx-post="/wikis/{{wiki.slug}}/upload-media"
                            hx-include="#media-file"
                            hx-target="#media-preview"
                            hx-swap="beforeend">
                        <i class="fas fa-upload"></i> Upload
                    </button>
                </div>
                
                <div class="media-preview" id="media-preview">
                    % if page and media:
                    % for item in media:
                    <div class="media-preview-item">
                        % if item.mime_type.startswith('image'):
                        <img src="/media/{{item.wiki_id}}/{{item.uuid_filename}}" alt="{{item.original_filename}}">
                        % else:
                        <div class="bg-gray-200 p-2 text-center">
                            <i class="fas fa-file text-2xl"></i>
                            <p class="truncate text-xs">{{item.original_filename}}</p>
                        </div>
                        % end
                        <input type="hidden" name="attached_media[]" value="{{item.id}}">
                        <button type="button" class="remove-media" 
                                hx-delete="/media/delete/{{item.id}}"
                                hx-target="closest .media-preview-item"
                                hx-swap="delete">
                            <i class="fas fa-times"></i>
                        </button>
                    </div>
                    % end
                    % end
                </div>
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
    
<script>
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

// Simple editor toolbar functionality
document.querySelectorAll('.editor-toolbar button').forEach(button => {
    button.addEventListener('click', function() {
        const command = this.dataset.command;
        const textarea = document.getElementById('content');
        const start = textarea.selectionStart;
        const end = textarea.selectionEnd;
        const selectedText = textarea.value.substring(start, end);
        
        let newText = '';
        switch(command) {
            case 'bold':
                newText = `**${selectedText}**`;
                break;
            case 'italic':
                newText = `_${selectedText}_`;
                break;
            case 'heading':
                newText = `# ${selectedText}`;
                break;
            case 'link':
                newText = `[${selectedText}](url)`;
                break;
            case 'image':
                newText = `![${selectedText || 'description'}](image-url)`;
                break;
            case 'code':
                newText = selectedText.includes('\n') 
                    ? `\`\`\`\n${selectedText}\n\`\`\`` 
                    : `\`${selectedText}\``;
                break;
            case 'unordered-list':
                newText = selectedText.split('\n').map(line => `- ${line}`).join('\n');
                break;
            default:
                return;
        }
        
        textarea.value = textarea.value.substring(0, start) + 
                         newText + 
                         textarea.value.substring(end);
        
        // Refocus and set cursor position
        textarea.focus();
        textarea.setSelectionRange(start, start + newText.length);
    });
});
</script>/script>
