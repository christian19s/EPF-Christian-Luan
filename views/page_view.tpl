% rebase('layout', title=page.title)
<link rel="stylesheet" href="/static/css/style.css">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.7.0/styles/github.min.css">
<script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.7.0/highlight.min.js"></script>
<script>hljs.highlightAll();</script>
<script src="/static/js/dark-mode.js"></script>

<div class="container">
    <nav class="breadcrumb mb-md">
        <a href="/wikis">Wikis</a> &raquo;
        <a href="/wikis/{{wiki.slug}}">{{wiki.name}}</a> &raquo;
        <span>{{page.title}}</span>
    </nav>
    
    <div class="page-header">
        <div class="flex justify-between items-center">
            <h1 class="page-title">{{page.title}}</h1>
            
            % if can_edit:
                <a href="/wikis/{{wiki.slug}}/{{page.slug}}/edit" class="btn">
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
                    Last edited by {{last_editor_username}} on {{page.updated_at[:10]}}
                </span>
            % end
        </div>
    </div>
    
    <div class="content-body">
        {{! rendered_content }}
    </div>
    
    % if media:
    <div class="page-media mt-5">
        <h3>Attachments</h3>
        <div class="grid grid-cols-3 gap-4">
            % for item in media:
                % if item.mime_type.startswith('image'):
                <div class="media-item">
                    <img src="/media/{{item.wiki_id}}/{{item.uuid_filename}}" 
                         alt="{{item.original_filename}}" 
                         class="img-thumbnail">
                </div>
                % else:
                <div class="media-item">
                    <a href="/media/{{item.wiki_id}}/{{item.uuid_filename}}" 
                       class="flex items-center">
                        <i class="fas fa-file mr-2"></i>
                        {{item.original_filename}}
                    </a>
                </div>
                % end
            % end
        </div>
    </div>
    % end
</div>
