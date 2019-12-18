import Buefy from 'buefy';
import Vue from 'vue';
import { VueMasonryPlugin } from 'vue-masonry';
import App from './App.vue';
import router from './router';
import setUpAxiosCsrfConfig from './components/utils/csrf';
import './registerServiceWorker';

Vue.config.productionTip = false;
Vue.use(Buefy);
Vue.use(VueMasonryPlugin);
setUpAxiosCsrfConfig();

new Vue({
  router,
  render: h => h(App),
}).$mount('#app');
