% rebase('layout', title='Login')

<link rel="stylesheet" href="/static/css/login.css">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">

<div class="login-page">
    <div class="login-container">
        <h2><i class="fas fa-sign-in-alt"></i> Faça Login</h2>
        
        % if error:
            <div class="alert alert-error">
                <i class="fas fa-exclamation-circle"></i> {{ error }}
            </div>
        % end

        <form action="/login" method="POST">
            <div class="form-group">
                <label for="username"><i class="fas fa-user"></i> Usuário:</label>
                <input type="text" id="username" name="username" required class="form-control" placeholder="Digite seu usuário">
            </div>
            
            <div class="form-group password-toggle">
                <label for="password"><i class="fas fa-lock"></i> Senha:</label>
                <input type="password" id="password" name="password" required class="form-control" placeholder="Digite sua senha">
                <button type="button" class="toggle-password" onclick="togglePassword()">
                    <i class="fas fa-eye"></i>
                </button>
            </div>
            
            <div class="form-group">
                <button type="submit" class="btn">
                    <i class="fas fa-sign-in-alt"></i> Entrar
                </button>
            </div>
            
            <div class="form-links">
                <a href="/forgot-password"><i class="fas fa-key"></i> Esqueceu a senha?</a>
                <a href="/register"><i class="fas fa-user-plus"></i> Criar nova conta</a>
            </div>
        </form>
    </div>
</div>

<script>
    function togglePassword() {
        const passwordField = document.getElementById('password');
        const icon = document.querySelector('.toggle-password i');
        if (passwordField.type === 'password') {
            passwordField.type = 'text';
            icon.classList.replace('fa-eye', 'fa-eye-slash');
        } else {
            passwordField.type = 'password';
            icon.classList.replace('fa-eye-slash', 'fa-eye');
        }
    }
</script>