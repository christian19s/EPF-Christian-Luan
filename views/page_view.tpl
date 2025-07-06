% rebase('layout', title=page.title)
<link rel="stylesheet" href="/static/css/style.css">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.7.0/styles/github.min.css">
<script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.7.0/highlight.min.js"></script>
<script>hljs.highlightAll();</script>
<script src="/static/js/dark-mode.js"></script>

<style>
  .wiki-page-container {
    max-width: 900px;
    margin: 2rem auto;
    background: var(--surface-1);
    border-radius: 8px;
    overflow: hidden;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  }

  .page-header {
    padding: 1.5rem 2rem;
    background: var(--surface-2);
    border-bottom: 1px solid var(--border-color);
  }

  .page-title {
    margin: 0;
    font-size: 2.2rem;
    font-weight: 500;
    color: var(--text-primary);
  }

  .page-meta {
    margin-top: 0.5rem;
    font-size: 0.9rem;
    color: var(--text-secondary);
    font-style: italic;
  }

  .page-content-container {
    padding: 2rem;
  }

  .wikipedia-style {
    font-family: 'Georgia', serif;
    font-size: 1.1rem;
    line-height: 1.7;
    color: var(--text-primary);
  }

  .wikipedia-style h1,
  .wikipedia-style h2,
  .wikipedia-style h3,
  .wikipedia-style h4,
  .wikipedia-style h5 {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    font-weight: 500;
    color: var(--text-primary);
    border-bottom: 1px solid var(--border-color);
    padding-bottom: 0.3em;
  }

  .wikipedia-style h2 {
    font-size: 1.8rem;
    margin-top: 1.8em;
  }

  .wikipedia-style h3 {
    font-size: 1.5rem;
  }

  .wikipedia-style a {
    color: var(--link);
    text-decoration: none;
  }

  .wikipedia-style a:hover {
    text-decoration: underline;
  }

  .wikipedia-style code {
    background: var(--surface-2);
    padding: 0.2em 0.4em;
    border-radius: 4px;
    font-family: 'Fira Code', monospace;
  }

  .wikipedia-style pre {
    background: var(--surface-2);
    padding: 1rem;
    border-radius: 6px;
    overflow-x: auto;
    border-left: 3px solid var(--accent);
  }

  .wikipedia-style blockquote {
    border-left: 3px solid var(--border-color);
    padding-left: 1rem;
    margin-left: 0;
    color: var(--text-secondary);
  }

  .wikipedia-style table {
    width: 100%;
    border-collapse: collapse;
    margin: 1.5rem 0;
  }

  .wikipedia-style th {
    background: var(--surface-2);
    font-weight: 600;
    text-align: left;
  }

  .wikipedia-style th, 
  .wikipedia-style td {
    padding: 0.75rem;
    border: 1px solid var(--border-color);
  }

  .media-header {
    margin: 2rem 0 1rem;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid var(--border-color);
  }

  .media-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
    gap: 1.5rem;
  }

  .media-item {
    background: var(--surface-2);
    border-radius: 6px;
    overflow: hidden;
    transition: transform 0.2s;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  }

  .media-item:hover {
    transform: translateY(-3px);
  }

  .media-thumbnail img {
    width: 100%;
    height: 120px;
    object-fit: cover;
    display: block;
  }

  .media-name {
    padding: 0.75rem;
    font-size: 0.85rem;
    text-align: center;
    word-break: break-all;
    color: var(--text-primary);
  }

  .media-link {
    display: block;
    color: var(--text-primary);
    text-decoration: none;
    text-align: center;
    padding: 1rem;
  }

  .media-icon {
    font-size: 2rem;
    margin-bottom: 0.5rem;
    color: var(--accent);
  }

  .page-footer {
    padding: 1.5rem 2rem;
    background: var(--surface-2);
    border-top: 1px solid var(--border-color);
  }

  .footer-actions {
    display: flex;
    gap: 1rem;
    justify-content: center;
  }

  .btn-edit {
    background: var(--primary);
    color: var(--text-on-primary);
  }

  .btn-edit:hover {
    background: var(--primary-hover);
  }

  .btn {
    padding: 0.75rem 1.5rem;
    border-radius: 6px;
    font-weight: 500;
    cursor: pointer;
    border: none;
    transition: all 0.2s;
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 1rem;
    background: var(--surface-3);
    color: var(--text-primary);
  }

  .btn:hover {
    background: var(--surface-4);
  }
</style>

<div class="wiki-page-container">
    <nav class="breadcrumb mb-md">
        <a href="/wikis">Wikis</a> &raquo;
        <a href="/wikis/{{wiki.slug}}">{{wiki.name}}</a> &raquo;
        <span>{{page.title}}</span>
    </nav>
    
    <div class="page-header">
        <div class="flex justify-between items-center">
            <h1 class="page-title">{{page.title}}</h1>
            
            % if can_edit:
                <a href="/wikis/{{wiki.slug}}/{{page.slug}}/edit" class="btn btn-edit">
                    <i class="fas fa-edit"></i> Edit Page
                </a>
            % end
        </div>
        
        <div class="page-meta">
            <span>
                Created by {{author_username}} on {{page.created_at[:10]}}
            </span>
            % if last_editor_username:
                <span>
                    • Last edited by {{last_editor_username}} on {{page.updated_at[:10]}}
                </span>
            % end
        </div>
    </div>
    
    <div class="page-content-container">
        <div class="content-body wikipedia-style">
            {{! rendered_content }}
        </div>
        
        % if media:
        <div class="page-media mt-5">
            <div class="media-header">
                <h3><i class="fas fa-paperclip"></i> Attachments</h3>
            </div>
            <div class="media-grid">
                % for item in media:
                    % if item.mime_type.startswith('image'):
                    <div class="media-item">
                        <div class="media-thumbnail">
                            <img src="/media/{{item.wiki_id}}/{{item.uuid_filename}}" 
                                 alt="{{item.alt_text or item.original_filename}}">
                        </div>
                        <div class="media-name">{{item.original_filename}}</div>
                    </div>
                    % else:
                    <div class="media-item">
                        <a href="/media/{{item.wiki_id}}/{{item.uuid_filename}}" 
                           class="media-link" download>
                            <div class="media-icon">
                                <i class="fas fa-file"></i>
                            </div>
                            <div class="media-name">{{item.original_filename}}</div>
                        </a>
                    </div>
                    % end
                % end
            </div>
        </div>
        % end
    </div>
    
    <div class="page-footer">
        <div class="footer-actions">
            % if can_edit:
                <a href="/wikis/{{wiki.slug}}/{{page.slug}}/edit" class="btn btn-edit">
                    <i class="fas fa-edit"></i> Edit Page
                </a>
            % end
            <a href="/wikis/{{wiki.slug}}" class="btn">
                <i class="fas fa-book"></i> Back to Wiki
            </a>
        </div>
    </div>
</div>
