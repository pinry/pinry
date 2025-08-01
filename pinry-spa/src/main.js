import { createApp } from 'vue';
import App from './App.vue';
import { createI18n } from 'vue-i18n';
import localeUtils from './components/utils/i18n';
import router from './router';

const i18n = createI18n({
  locale: localStorage.getItem('localeCode') || navigator.language.split('-')[0],
  allowComposition: true,
  fallbackLocale: 'en',
  messages: localeUtils.messages,
});

const pinry = createApp(App);
pinry.use(router);
pinry.use(i18n);

pinry.mount('#app');

import Buefy from 'buefy';
import { VueMasonryPlugin } from 'vue-masonry';
import setUpAxiosCsrfConfig from './components/utils/csrf';
import './registerServiceWorker';

Vue.use(Buefy);
Vue.use(VueMasonryPlugin);
setUpAxiosCsrfConfig();


