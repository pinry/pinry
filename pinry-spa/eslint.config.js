import js from '@eslint/js';
import stylistic from '@stylistic/eslint-plugin';
import pluginVue from 'eslint-plugin-vue';
import globals from 'globals';

export default [
  {
    ignores: ['dist/**', 'node_modules/**'],
  },
  js.configs.recommended,
  ...pluginVue.configs['flat/recommended'],
  // Airbnb-like layout: 2-space indent, semicolons, single quotes, trailing commas.
  stylistic.configs.customize({
    indent: 2,
    quotes: 'single',
    semi: true,
    commaDangle: 'always-multiline',
    braceStyle: '1tbs',
    quoteProps: 'as-needed',
    arrowParens: false,
  }),
  {
    languageOptions: {
      ecmaVersion: 'latest',
      sourceType: 'module',
      globals: {
        ...globals.browser,
      },
    },
    rules: {
      'no-console': ['warn', { allow: ['warn', 'error'] }],
      'no-param-reassign': ['error', { props: true }],
      'prefer-const': 'error',
      'no-var': 'error',
      'object-shorthand': 'error',
      'prefer-template': 'error',
      eqeqeq: ['error', 'always'],
      '@stylistic/arrow-parens': ['error', 'as-needed', { requireForBlockBody: true }],
      '@stylistic/no-multiple-empty-lines': ['error', { max: 2, maxEOF: 0 }],
      '@stylistic/quotes': ['error', 'single', { avoidEscape: true }],
      '@stylistic/max-len': ['error', {
        code: 100,
        ignoreStrings: true,
        ignoreTemplateLiterals: true,
        ignoreUrls: true,
        // Long template lines are mostly attribute lists and i18n calls.
        ignorePattern: '^\\s*<',
      }],
      'no-unused-vars': ['error', { caughtErrors: 'none', ignoreRestSiblings: true }],
      // Templates keep their existing attribute layout.
      'vue/max-attributes-per-line': 'off',
      'vue/singleline-html-element-content-newline': 'off',
      'vue/multiline-html-element-content-newline': 'off',
      'vue/html-closing-bracket-newline': 'off',
      'vue/html-indent': 'off',
      'vue/html-self-closing': 'off',
      'vue/attribute-hyphenation': 'off',
      'vue/v-on-event-hyphenation': 'off',
      'vue/attributes-order': 'off',
      'vue/order-in-components': 'off',
      'vue/first-attribute-linebreak': 'off',
      'vue/v-bind-style': 'off',
      'vue/v-on-style': 'off',
      'vue/require-prop-types': 'off',
      'vue/multi-word-component-names': 'off',
      'vue/component-definition-name-casing': 'off',
      // v-html is allowed only through niceLinks, which escapes everything.
      'vue/no-v-html': 'off',
    },
  },
  {
    files: ['vite.config.js', 'eslint.config.js'],
    languageOptions: {
      globals: { ...globals.node },
    },
  },
];
