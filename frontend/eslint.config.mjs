import { defineConfig } from 'eslint/config';

export default defineConfig([
  {
    files: ['**/*.js'],
    languageOptions: {
      globals: { window: true, document: true },
      sourceType: 'module',
    },
    extends: ['eslint:recommended', 'plugin:prettier/recommended'],
  },
]);
 