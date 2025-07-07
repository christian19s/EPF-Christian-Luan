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
        % if user:
            <button id="btnDashboard" class="login-button">
                <i class="fas fa-tachometer-alt"></i> Dashboard
            </button>
        % else:
            <button id="btnLogin" class="login-button">
                <i class="fas fa-sign-in-alt"></i> Login
            </button>
        % end
    </div>
    
    <div class="main">
        <div class="link-table">
            <h3><i class="fas fa-clock"></i>Wikis Recentes</h3>
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
                        <p>Nenhuma wiki encontrada</p>
                        <a href="/wikis/create" class="create-link">Criar uma wiki agora</a>
                    </div>
                % end
            </div>
        </div>
        
        <div class="main-p">
            <h2>Bem-vindo a WikiTree</h2>
            <p>Crie wikis e contribua com wikis existentes. </p>
            <p>Comece criando sua própria ou pesquise por existentes para colaborar.</p>
        </div>
    </div>
    
    <div class="wiki-buttons">
        <button id="btnCreate" class="create-button">
            <i class="fas fa-plus"></i> Criar Wiki
        </button>
        <button id="btnView" class="view-button">
            <i class="fas fa-book"></i> Todas as Wikis
        </button>
    </div>
    
    <button id="themeToggle" title="Toggle Dark Mode">
        <i class="fas fa-moon"></i>
    </button>
    
    <footer>
        <p>© 2025, WikiTree. Todos os direitos reservados.</p>
    </footer>
    
<script>
    // Wait for DOM to be fully loaded
    document.addEventListener('DOMContentLoaded', function() {
        // Create Wiki button
        const btnCreate = document.getElementById('btnCreate');
        if (btnCreate) {
            btnCreate.addEventListener('click', function() {
                window.location.href = '/wikis/create';
            });
        }
        
        // View All Wikis button
        const btnView = document.getElementById('btnView');
        if (btnView) {
            btnView.addEventListener('click', function() {
                window.location.href = '/wikis';
            });
        }
        
        // Check which button exists (login or dashboard)
        const btnDashboard = document.getElementById('btnDashboard');
        const btnLogin = document.getElementById('btnLogin');
        
        if (btnDashboard) {
            btnDashboard.addEventListener('click', function() {
                window.location.href = '/dashboard';
            });
        }
        
        if (btnLogin) {
            btnLogin.addEventListener('click', function() {
                window.location.href = '/login';
            });
        }
        
        // Theme toggle button
        const themeToggle = document.getElementById('themeToggle');
        if (themeToggle) {
            themeToggle.addEventListener('click', function() {
                // This should be handled by your dark-mode.js
                console.log('Theme toggle clicked');
            });
        }
    });
</script>
</body>
</html>