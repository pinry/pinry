import { createI18n } from 'vue-i18n';
import en from './locales/en.json';
import zh from './locales/zh.json';
import fr from './locales/fr.json';

const messages = {
  en,
  zh,
  fr,
};

const langCode2Name = {
  en: 'English',
  zh: '简体中文',
  fr: 'Français',
};

const storageKey = 'localeCode';

function initialLocale() {
  const saved = localStorage.getItem(storageKey);
  if (saved in messages) return saved;
  const browser = navigator.language.split('-')[0];
  return browser in messages ? browser : 'en';
}

// Composition mode; $t and $i18n stay available in every template.
const i18n = createI18n({
  legacy: false,
  globalInjection: true,
  locale: initialLocale(),
  fallbackLocale: 'en',
  messages,
});

document.documentElement.lang = i18n.global.locale.value;

function setLocale(locale) {
  i18n.global.locale.value = locale;
  document.documentElement.lang = locale;
  localStorage.setItem(storageKey, locale);
}

export default i18n;
export {
  langCode2Name,
  setLocale,
};
