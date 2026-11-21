import { fileURLToPath, URL } from 'node:url';
import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';

// Keep the browser's Host header, as nginx does in production: Django 4+
// checks the Origin of unsafe requests against it for CSRF.
const backend = {
  target: 'http://127.0.0.1:8000/',
};

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
    },
  },
  server: {
    proxy: {
      '/api': { ...backend, ws: true },
      '/admin': backend,
      '/media': backend,
      '/static/': backend,
    },
  },
  build: {
    // nginx serves pinry-spa/dist for "/"
    outDir: 'dist',
  },
});
