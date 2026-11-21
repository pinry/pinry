// Light / dark theme. 'system' follows the OS setting, also when it changes
// while the page is open. public/theme-init.js applies the saved choice before
// the app loads; keep its storage key and values in step with this file.
const storageKey = 'theme';
const themes = ['light', 'dark', 'system'];
const darkQuery = window.matchMedia('(prefers-color-scheme: dark)');

function getTheme() {
  let saved = null;
  try {
    saved = localStorage.getItem(storageKey);
  } catch {
    // Storage can be blocked; use the default.
  }
  return themes.includes(saved) ? saved : 'system';
}

function applyTheme(theme) {
  let resolved = theme;
  if (theme === 'system') {
    resolved = darkQuery.matches ? 'dark' : 'light';
  }
  document.documentElement.dataset.theme = resolved;
}

function setTheme(theme) {
  try {
    localStorage.setItem(storageKey, theme);
  } catch {
    // Storage can be blocked; the choice then lasts until the page reloads.
  }
  applyTheme(theme);
}

function initTheme() {
  applyTheme(getTheme());
  darkQuery.addEventListener('change', () => {
    if (getTheme() === 'system') {
      applyTheme('system');
    }
  });
}

export {
  themes,
  getTheme,
  setTheme,
  initTheme,
};
