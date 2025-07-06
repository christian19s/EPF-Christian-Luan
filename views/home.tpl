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
            <h3>Recent Wikis</h3>
            <ul id="wiki-list">
                <!-- Dynamic content will be inserted here -->
                <li>Example Wiki 1</li>
                <li>Example Wiki 2</li>
            </ul>
        </div>
        
        <div class="main-p">
            <h2>Welcome to WikiTree</h2>
            <p>Create and collaborate on wikis with your community. WikiTree provides an easy way to organize and share knowledge in a tree-like structure.</p>
            <p>Start by creating your own wiki or browse existing ones to contribute.</p>
        </div>
    </div>
    
    <div class="wiki-buttons">
        <button id="btnCreate" class="create-button">
            <i class="fas fa-plus"></i> Criar Wiki
        </button>
        <button id="btnView" class="view-button">
            <i class="fas fa-book"></i> Ver Wikis
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