import Buefy from 'buefy';
import Vue from 'vue';
import { VueMasonryPlugin } from 'vue-masonry';
import App from './App.vue';
import router from './router';


Vue.config.productionTip = false;
Vue.use(Buefy);
Vue.use(VueMasonryPlugin);

new Vue({
  router,
  render: h => h(App),
}).$mount('#app');
