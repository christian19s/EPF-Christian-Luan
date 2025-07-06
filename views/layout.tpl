<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{title}}</title>
    <link rel="stylesheet" href="/static/css/theme.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <script src="https://unpkg.com/htmx.org@1.9.6"></script>
    <script src="/static/js/dark-mode.js"></script>
</head>
<body>
    <div class="container">
        <!-- Theme toggle in header -->
        <div class="dashboard-header">
            <div class="header-left">
                <a href="/" class="home-button" title="Return to Home">
                    <i class="fas fa-home"></i>
                </a>
                <h1>{{title}}</h1>
            </div>
            <div class="theme-toggle" id="themeToggle">
                <i class="fas fa-moon"></i>
                <span id="themeText">Dark Mode</span>
            </div>
        </div>
        
        <!-- Content will be inserted here -->
        {{!base}}
    </div>
    
    <script>
        document.addEventListener('DOMContentLoaded', function() {
            // Initialize theme manager
            ThemeManager.init();
        });
    </script>
</body>
</html>
