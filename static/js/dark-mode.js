//modo escuro configuravel
const DarkMode = (function() {
    const STORAGE_KEY = 'theme';
    const DARK_MODE_CLASS = 'dark-mode';
    const THEME_TOGGLE_ID = 'themeToggle';
    const THEME_TEXT_ID = 'themeText';
    

    let themeToggle, themeText;
    
    function init() {
        themeToggle = document.getElementById(THEME_TOGGLE_ID);
        themeText = document.getElementById(THEME_TEXT_ID);
        
        if (!themeToggle || !themeText) {
            console.error('Dark Mode: Required elements not found');
            return;
        }
        
        applyTheme();
        
        themeToggle.addEventListener('click', toggleTheme);
    }
    
    function applyTheme() {
        const savedTheme = localStorage.getItem(STORAGE_KEY);
        const systemPrefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
        
        if (savedTheme === 'dark' || (!savedTheme && systemPrefersDark)) {
            enableDarkMode();
        } else {
            disableDarkMode();
        }
    }
    
    function toggleTheme() {
        if (document.body.classList.contains(DARK_MODE_CLASS)) {
            disableDarkMode();
        } else {
            enableDarkMode();
        }
    }
    
    function enableDarkMode() {
        document.body.classList.add(DARK_MODE_CLASS);
        themeText.textContent = 'Light Mode';
        themeToggle.querySelector('i').className = 'fas fa-sun';
        localStorage.setItem(STORAGE_KEY, 'dark');
        
        document.dispatchEvent(new CustomEvent('darkModeChange', {
            detail: { mode: 'dark' }
        }));
    }
    
    function disableDarkMode() {
        document.body.classList.remove(DARK_MODE_CLASS);
        themeText.textContent = 'Dark Mode';
        themeToggle.querySelector('i').className = 'fas fa-moon';
        localStorage.setItem(STORAGE_KEY, 'light');
        
        document.dispatchEvent(new CustomEvent('darkModeChange', {
            detail: { mode: 'light' }
        }));
    }
    
    // api 
    return {
        init: init,
        enable: enableDarkMode,
        disable: disableDarkMode,
        toggle: toggleTheme
    };
})();

document.addEventListener('DOMContentLoaded', DarkMode.init);
