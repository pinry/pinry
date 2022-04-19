import Buefy from 'buefy';
import Vue from 'vue';
import { VueMasonryPlugin } from 'vue-masonry';
import VueI18n from 'vue-i18n';
import App from './App.vue';
import router from './router';
import setUpAxiosCsrfConfig from './components/utils/csrf';
import './registerServiceWorker';
import en from './assets/locales/en.json';

const messages = {
  en,
};

Vue.config.productionTip = false;
Vue.use(Buefy);
Vue.use(VueMasonryPlugin);
Vue.use(VueI18n);
setUpAxiosCsrfConfig();

const i18n = new VueI18n({
  locale: localStorage.getItem('localeCode') || navigator.language.split('-')[0],
  fallbackLocale: 'en',
  messages,
});

new Vue({
  router,
  i18n,
  render: h => h(App),
}).$mount('#app');
