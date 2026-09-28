import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import tailwindcss from '@tailwindcss/vite';
import { fileURLToPath } from 'node:url';

export default defineConfig({
  plugins: [react(), tailwindcss()],
  resolve: { alias: { '~@ibm/plex': fileURLToPath(new URL('./node_modules/@ibm/plex', import.meta.url)) } },
  // Carbon owns its Sass deprecations; keep warnings for application Sass visible.
  css: { preprocessorOptions: { scss: { quietDeps: true } } },
});
