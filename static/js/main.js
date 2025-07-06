/**
 * Efeitos Visuais para o Sistema Bottle
 * 
 * Inclui:
 * - Animação de carregamento suave
 * - Efeito de hover em botões/tabelas
 * - Feedback visual para formulários
 * - Botão de scroll para topo
 */

document.addEventListener('DOMContentLoaded', function() {
    console.log('Página carregada no navegador!')
    
    // 1. Efeito de fade-in ao carregar a página
    document.body.style.opacity = '0';
    setTimeout(() => {
        document.body.style.transition = 'opacity 0.5s ease-in-out';
        document.body.style.opacity = '1';
    }, 100);

});

    function togglePassword(id) {
        const input = document.getElementById(id);
        const icon = input.nextElementSibling.querySelector('i');
        if (input.type === 'password') {
            input.type = 'text';
            icon.classList.replace('fa-eye', 'fa-eye-slash');
        } else {
            input.type = 'password';
            icon.classList.replace('fa-eye-slash', 'fa-eye');
        }
    }

    function checkPasswordStrength(password) {
        const strengthMeter = document.getElementById('strengthMeter');
        const requirements = {
            length: password.length >= 8,
            uppercase: /[A-Z]/.test(password),
            lowercase: /[a-z]/.test(password),
            number: /[0-9]/.test(password),
            special: /[^A-Za-z0-9]/.test(password)
        };

        // Update requirement indicators
        document.getElementById('length-req').className = requirements.length ? 'valid' : '';
        document.getElementById('uppercase-req').className = requirements.uppercase ? 'valid' : '';
        document.getElementById('lowercase-req').className = requirements.lowercase ? 'valid' : '';
        document.getElementById('number-req').className = requirements.number ? 'valid' : '';
        document.getElementById('special-req').className = requirements.special ? 'valid' : '';

        // Calculate strength score (0-4)
        const strength = Object.values(requirements).filter(Boolean).length;
        const strengthPercent = (strength / 4) * 100;

        // Update strength meter
        strengthMeter.style.width = `${strengthPercent}%`;
        strengthMeter.style.backgroundColor = getStrengthColor(strength);
    }

    function getStrengthColor(strength) {
        switch(strength) {
            case 0:
            case 1:
                return 'var(--red)';
            case 2:
                return 'var(--peach)';
            case 3:
                return 'var(--yellow)';
            case 4:
                return 'var(--green)';
            default:
                return 'var(--surface0)';
        }
    }

    function checkPasswordMatch() {
        const newPassword = document.getElementById('new_password').value;
        const confirmPassword = document.getElementById('confirm_password').value;
        const matchText = document.getElementById('passwordMatch');

        if (!newPassword || !confirmPassword) {
            matchText.textContent = '';
            return;
        }

        if (newPassword === confirmPassword) {
            matchText.textContent = 'Passwords match';
            matchText.style.color = 'var(--green)';
        } else {
            matchText.textContent = 'Passwords do not match';
            matchText.style.color = 'var(--red)';
        }
    }

    document.addEventListener('DOMContentLoaded', function() {
        // Initialize password strength check
        document.getElementById('new_password').dispatchEvent(new Event('input'));
    });
