const ThemeManager = (function() {
    const STORAGE_KEY = 'theme';
    const THEME_TOGGLE_ID = 'themeToggle';
    const THEME_TEXT_ID = 'themeText';
    
    // Catppuccin Mocha  palette
    const MOCHA_THEME = {
        '--base': '#1e1e2e',
        '--mantle': '#181825',
        '--crust': '#11111b',
        '--surface0': '#313244',
        '--surface1': '#45475a',
        '--surface2': '#585b70',
        '--text': '#cdd6f4',
        '--subtext0': '#a6adc8',
        '--subtext1': '#bac2de',
        '--mauve': '#cba6f7',
        '--lavender': '#b4befe',
        '--blue': '#89b4fa',
        '--red': '#f38ba8',
        '--green': '#a6e3a1',
        '--yellow': '#f9e2af',
        '--peach': '#fab387',
    };

    //  (light theme) palette
    const GRUVBOX_THEME = {
        '--base': '#fbf1c7',
        '--mantle': '#f2e5bc',
        '--crust': '#ebdbb2',
        '--surface0': '#d5c4a1',
        '--surface1': '#bdae93',
        '--surface2': '#a89984',
        '--text': '#3c3836',
        '--subtext0': '#665c54',
        '--subtext1': '#7c6f64',
        '--mauve': '#b16286',
        '--lavender': '#8f3f71',
        '--blue': '#458588',
        '--red': '#cc241d',
        '--green': '#98971a',
        '--yellow': '#d79921',
        '--peach': '#d65d0e',
    };

    let themeToggle, themeText;
    
    function init() {
        themeToggle = document.getElementById(THEME_TOGGLE_ID);
        themeText = document.getElementById(THEME_TEXT_ID);
        
        if (!themeToggle || !themeText) {
            console.error('Theme Manager: Required elements not found');
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
            enableLightMode();
        }
    }
    
    function toggleTheme() {
        if (document.body.classList.contains('dark-mode')) {
            enableLightMode();
        } else {
            enableDarkMode();
        }
    }
    
    function setThemeVariables(theme) {
        for (const [key, value] of Object.entries(theme)) {
            document.documentElement.style.setProperty(key, value);
        }
    }
    
    function enableDarkMode() {
        document.body.classList.add('dark-mode');
        document.body.classList.remove('light-mode');
        themeText.textContent = 'Light Mode';
        themeToggle.querySelector('i').className = 'fas fa-sun';
        localStorage.setItem(STORAGE_KEY, 'dark');
        setThemeVariables(MOCHA_THEME);
        
        document.dispatchEvent(new CustomEvent('themeChange', {
            detail: { mode: 'dark' }
        }));
    }
    
    function enableLightMode() {
        document.body.classList.add('light-mode');
        document.body.classList.remove('dark-mode');
        themeText.textContent = 'Dark Mode';
        themeToggle.querySelector('i').className = 'fas fa-moon';
        localStorage.setItem(STORAGE_KEY, 'light');
        setThemeVariables(GRUVBOX_THEME);
        
        document.dispatchEvent(new CustomEvent('themeChange', {
            detail: { mode: 'light' }
        }));
    }
    
    return {
        init: init,
        enableDarkMode: enableDarkMode,
        enableLightMode: enableLightMode,
        toggle: toggleTheme
    };
})();
//AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAHHHH
document.addEventListener('DOMContentLoaded', ThemeManager.init);
