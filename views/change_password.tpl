% rebase('layout', title='Change Password')
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
<script src="https://unpkg.com/htmx.org@1.9.6"></script>
<script src="/static/js/dark-mode.js"></script>

<link rel="stylesheet" href="/static/css/change-password.css"/>

<div class="htmx-indicator">
    <i class="fas fa-spinner fa-spin"></i> Updating password...
</div>

<div class="password-container">
    <div class="password-header">
        <h1><i class="fas fa-lock"></i> Change Password</h1>
        <p>Secure your account with a new password</p>
    </div>

    % if get('success'):
        <div class="alert alert-success">
            <i class="fas fa-check-circle"></i> {{success}}
        </div>
    % end
    % if get('error'):
        <div class="alert alert-error">
            <i class="fas fa-exclamation-circle"></i> {{error}}
        </div>
    % end

    <form class="password-form" 
          hx-post="/change-password" 
          hx-target=".password-container" 
          hx-swap="outerHTML"
          hx-indicator=".htmx-indicator">
        
        <div class="form-group">
            <label for="current_password">Current Password</label>
            <div class="input-wrapper">
                <input type="password" 
                       id="current_password" 
                       name="current_password" 
                       required
                       autocomplete="current-password">
                <button type="button" class="toggle-password" onclick="togglePassword('current_password')">
                    <i class="fas fa-eye"></i>
                </button>
            </div>
        </div>

        <div class="form-group">
            <label for="new_password">New Password</label>
            <div class="input-wrapper">
                <input type="password" 
                       id="new_password" 
                       name="new_password" 
                       required
                       autocomplete="new-password"
                       oninput="checkPasswordStrength(this.value)">
                <button type="button" class="toggle-password" onclick="togglePassword('new_password')">
                    <i class="fas fa-eye"></i>
                </button>
            </div>
            <div class="password-strength">
                <div class="strength-meter" id="strengthMeter"></div>
            </div>
            <ul class="password-requirements" id="passwordRequirements">
                <li id="length-req">At least 8 characters</li>
                <li id="uppercase-req">Contains uppercase letter</li>
                <li id="lowercase-req">Contains lowercase letter</li>
                <li id="number-req">Contains number</li>
                <li id="special-req">Contains special character</li>
            </ul>
        </div>

        <div class="form-group">
            <label for="confirm_password">Confirm New Password</label>
            <div class="input-wrapper">
                <input type="password" 
                       id="confirm_password" 
                       name="confirm_password" 
                       required
                       autocomplete="new-password"
                       oninput="checkPasswordMatch()">
                <button type="button" class="toggle-password" onclick="togglePassword('confirm_password')">
                    <i class="fas fa-eye"></i>
                </button>
            </div>
            <small id="passwordMatch" style="color: var(--subtext0);"></small>
        </div>

        <button type="submit" class="password-submit">
            <i class="fas fa-key"></i> Change Password
        </button>
    </form>
</div>

<script src="../static/js/main.js">
</script>