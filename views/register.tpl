<!-- views/register.tpl -->
% rebase('layout', title='Criar Conta')

<div class="login-container">
    <h2>Criar Nova Conta</h2>
    
    <form action="/register" method="POST">
        <div class="form-group">
            <label for="username">Usuário:</label>
            <input type="text" id="username" name="username" required class="form-control">
        </div>
        
        <div class="form-group">
            <label for="email">Email:</label>
            <input type="email" id="email" name="email" required class="form-control">
        </div>
        
        <div class="form-group">
            <label for="password">Senha:</label>
            <input type="password" id="password" name="password" required class="form-control">
        </div>
        
        <div class="form-group">
            <label for="confirm_password">Confirmar Senha:</label>
            <input type="password" id="confirm_password" name="confirm_password" required class="form-control">
        </div>
        
        <div class="form-group">
            <button type="submit" class="btn btn-primary">Criar Conta</button>
        </div>
        
        <div class="form-links">
            <a href="/login">Já tem uma conta? Faça login</a>
        </div>
    </form>
</div>
