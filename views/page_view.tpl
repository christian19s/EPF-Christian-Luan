% rebase('layout', title=page.title)
<link rel="stylesheet" href="/static/css/style.css">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.7.0/styles/github.min.css">
<script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.7.0/highlight.min.js"></script>
<script>hljs.highlightAll();</script>

<div class="container">
    <nav class="breadcrumb mb-md">
        <a href="/wikis">Wikis</a> &raquo;
        <a href="/wikis/{{wiki.slug}}">{{wiki.name}}</a> &raquo;
        <span>{{page.title}}</span>
    </nav>
    
    <div class="page-header">
        <div class="flex justify-between items-center">
            <h1 class="page-title">{{page.title}}</h1>
            
            % if page.can_edit(user):
                <a href="/wikis/{{wiki.slug}}/{{page.slug}}/edit" class="btn">
                    <i class="fas fa-edit"></i> Edit Page
                </a>
            % end
        </div>
        
        <div class="page-meta">
            <span>
                Created by {{page.author.username}} on {{page.created_at[:10]}}
            </span>
            <span>
                Last edited by {{page.last_editor.username}} on {{page.updated_at[:10]}}
            </span>
        </div>
    </div>
    
    <div class="content-body">
        {{! rendered_content }}
    </div>
    
    <div class="card mt-lg">
        <h2 class="section-title">Page History</h2>
        
        % if not history:
            <p>No edit history available</p>
        % else:
            <ul class="activity-list">
                % for edit in history:
                <li class="activity-item">
                    <div class="activity-icon">
                        <i class="fas fa-history"></i>
                    </div>
                    <div class="activity-content">
                        <div class="activity-title">
                            {{edit.user.username}} 
                            % if edit.edit_comment:
                                - {{edit.edit_comment}}
                            % end
                        </div>
                        <div class="activity-time">
                            {{edit.edit_time}}
                        </div>
                    </div>
                </li>
                % end
            </ul>
        % end
    </div>
</div>
