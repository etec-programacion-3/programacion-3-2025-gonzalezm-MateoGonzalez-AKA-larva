import { defineConfig } from 'eslint/config';

export default defineConfig([
  {
    files: ['**/*.{js,mjs,cjs}'],
    languageOptions: {
      globals: { NodeJS: true },
      sourceType: 'commonjs',
    },
    extends: ['eslint:recommended', 'plugin:prettier/recommended'],
  },
]);
