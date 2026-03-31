# Project general coding guidelines

## Code Style
- Use semantic HTML5 elements (header, main, section, article, etc.)
- Prefer modern JavaScript (ES6+) features like const/let, arrow functions, and template literals

## Naming Conventions
- Use PascalCase for component names, interfaces, and type aliases
- Use camelCase for variables, functions, and methods
- Prefix private class members with underscore (_)
- Use ALL_CAPS for constants

## Code Quality
- Use meaningful variable and function names that clearly describe their purpose
- Include helpful comments for complex logic
- Add error handling for user inputs and API calls

// Dark mode toggle functionality
const darkModeToggle = document.getElementById('darkModeToggle');
const htmlElement = document.documentElement;

// Initialize dark mode from localStorage
const isDarkMode = localStorage.getItem('darkMode') === 'true';
if (isDarkMode) {
  htmlElement.setAttribute('data-theme', 'dark');
}

// Toggle dark mode on button click
darkModeToggle.addEventListener('click', () => {
  const currentTheme = htmlElement.getAttribute('data-theme');
  const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
  
  htmlElement.setAttribute('data-theme', newTheme);
  localStorage.setItem('darkMode', newTheme === 'dark');
  darkModeToggle.textContent = newTheme === 'dark' ? '☀️' : '🌙';
});
