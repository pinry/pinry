// Runs in <head>, before the app, so the first paint already uses the saved
// theme. Keep the storage key and values in step with components/utils/theme.js.
(() => {
  let theme = null;
  try {
    theme = localStorage.getItem('theme');
  } catch {
    // Storage can be blocked; fall back to the OS setting.
  }
  if (theme !== 'light' && theme !== 'dark') {
    theme = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  }
  document.documentElement.dataset.theme = theme;
})();
