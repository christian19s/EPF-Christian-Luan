<!DOCTYPE html>
<html>
<head>
    <title>WikiTree - Home</title>
    <link rel="stylesheet" href="/static/css/home.css"/>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <script src="/static/js/dark-mode.js"></script>
</head>
<body>
    <div class="header">
        <p class="title">WikiTree</p>
        <img src="/static/img/placeholder.jpg" alt="WikiTree logo" style="height: 80px">
        <button id="btnLogin" class="login-button">
            <i class="fas fa-sign-in-alt"></i> Login
        </button>
    </div>
    
    <div class="main">
        <div class="link-table">
            <h3><i class="fas fa-clock"></i> Recent Wikis</h3>
            <div class="wiki-grid">
                % if recent_wikis:
                    % for wiki in recent_wikis:
                    <div class="wiki-card">
                        <a href="/wikis/{{ wiki['slug'] }}" class="wiki-link">
                            <div class="wiki-icon">
                                <i class="fas fa-book-open"></i>
                            </div>
                            <div class="wiki-content">
                                <h4>{{ wiki['name'] }}</h4>
                                <p class="wiki-meta">
                                    <span class="wiki-date">
                                        <i class="far fa-calendar-alt"></i> {{ wiki['created_at'].strftime('%b %d, %Y') }}
                                    </span>
                                    <span class="wiki-author">
                                        <i class="fas fa-user"></i> {{ wiki['owner_username'] }}
                                    </span>
                                </p>
                                % if wiki['description']:
                                <p class="wiki-description">{{ wiki['description'][:100] }}{% if len(wiki['description']) > 100 %}...{% end %}</p>
                                % end
                            </div>
                        </a>
                    </div>
                    % end
                % else:
                    <div class="empty-wikis">
                        <i class="fas fa-book"></i>
                        <p>No wikis created yet</p>
                        <a href="/wikis/create" class="create-link">Be the first to create one!</a>
                    </div>
                % end
            </div>
        </div>
        
        <div class="main-p">
            <h2>Welcome to WikiTree</h2>
            <p>Create and collaborate on wikis with your community. WikiTree provides an easy way to organize and share knowledge in a tree-like structure.</p>
            <p>Start by creating your own wiki or browse existing ones to contribute.</p>
        </div>
    </div>
    
    <div class="wiki-buttons">
        <button id="btnCreate" class="create-button">
            <i class="fas fa-plus"></i> Create Wiki
        </button>
        <button id="btnView" class="view-button">
            <i class="fas fa-book"></i> Browse All
        </button>
    </div>
    
    <button id="themeToggle" title="Toggle Dark Mode">
        <i class="fas fa-moon"></i>
    </button>
    
    <footer>
        <p>© 2025, WikiTree. Todos os direitos reservados.</p>
    </footer>
    
    <script>
        document.getElementById('btnCreate').addEventListener('click', function() {
            window.location.href = '/wikis/create';
        });
        
        document.getElementById('btnView').addEventListener('click', function() {
            window.location.href = '/wikis';
        });
        
        document.getElementById('btnLogin').addEventListener('click', function() {
            window.location.href = '/login';
        });
    </script>
</body>
</html>