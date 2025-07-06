<!DOCTYPE html>
<html>
<head>
    <title>WikiTree - Criar Wiki</title>
    <link rel="stylesheet" href="/static/css/home.css"/>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <script src="/static/js/dark-mode.js"></script>
</head>
<body>
    <form action="/wikis/create" method="post">
        <div class="header">
            <input type="text" name="nome" placeholder="Nome da Wiki" class="form-name" required>
        </div>
        
        <input type="text" name="titulo" placeholder="Título da Página Inicial" class="form-title" required>
        
        <div class="form-main">
            <div class="link-table">
                <h3>Páginas</h3>
                <div id="page-list">
                    <!-- Pages will be added here dynamically -->
                    <p>Sua primeira página será criada automaticamente</p>
                </div>
            </div>
            
            <textarea name="texto" placeholder="Conteúdo da Página Inicial..." class="form-description" required></textarea>
        </div>
        
        <div style="text-align: center;">
            <button type="submit" class="create-button">
                <i class="fas fa-save"></i> Criar Wiki
            </button>
        </div>
    </form>
    
    <button id="themeToggle" title="Toggle Dark Mode">
        <i class="fas fa-moon"></i>
    </button>
    
    <footer>
        <p>© 2025, WikiTree. Todos os direitos reservados.</p>
    </footer>
</body>
</html>