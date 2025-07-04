% rebase('layout', title='Login')
<style>
    /* Login Page Styles */

     body {

      background-image: url("https://i.gifer.com/origin/ba/ba105810faa1e0227a5a8877f7cb68ea_w200.gif"); 
     }
    .login-container {
        max-width: 400px;
        margin: 50px auto;
        padding: 30px;
        background: #fff;
        border-radius: 0px;
        box-shadow: 0 10px 10px rgba(0, 0, 0, 0.1);
    }

    .login-container h2 {
        text-align: center;
        margin-bottom: 20px;
        color: #181926;
    }

    .form-group {
        margin-bottom: 20px;
    }

    .form-group label {
        display: block;
        margin-bottom: 8px;
        font-weight: 500;
    }

    .form-control {
        width: 90%;
        padding: 10px 15px;
        border: 1px solid #ddd;
        border-radius: 4px;
        font-size: 16px;
        transition: border-color 0.3s;
    }

    .form-control:focus {
        border-color: #3498db;
        outline: none;
        box-shadow: 0 0 0 2px rgba(52, 152, 219, 0.2);
    }

    .btn {
        display: inline-block;
        padding: 12px 20px;
        background: #3498db;
        color: white;
        border: none;
        border-radius: 4px;
        cursor: pointer;
        font-size: 16px;
        width: 100%;
        transition: background 0.3s;
    }

    .btn-primary {
        background: #3498db;
    }

    .btn-primary:hover {
        background: #2980b9;
    }

    .alert {
        padding: 10px 15px;
        margin-bottom: 20px;
        border-radius: 4px;
    }

    .alert-error {
        background: #f8d7da;
        color: #721c24;
        border: 1px solid #f5c6cb;
    }

    .form-links {
        display: flex;
        justify-content: space-between;
        margin-top: 20px;
        flex-wrap: wrap;
    }

    .form-links a {
        color: #3498db;
        text-decoration: none;
        margin: 5px 0;
    }

    .form-links a:hover {
        text-decoration: underline;
    }

    /* Responsive adjustments */
    @media (max-width: 480px) {
        .login-container {
            padding: 20px;
            margin: 20px auto;
        }
        
        .form-links {
            flex-direction: column;
            align-items: center;
            gap: 10px;
        }
    }
</style>
<div class="login-container">
    <h2>Faça Login</h2>
    
    % if error:
        <div class="alert alert-error">
            {{ error }}
        </div>
    % end

    <form action="/login" method="POST">
        <div class="form-group">
            <label for="username">Usuário:</label>
            <input type="text" id="username" name="username" required class="form-control">
        </div>
        
        <div class="form-group">
            <label for="password">Senha:</label>
            <input type="password" id="password" name="password" required class="form-control">
        </div>
        
        <div class="form-group">
            <button type="submit" class="btn btn-primary">Entrar</button>
        </div>
        
        <div class="form-links">
            <a href="/forgot-password">Esqueceu a senha?</a>
            <a href="/register">Criar nova conta</a>
        </div>
    </form>
</div>


