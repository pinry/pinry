import Buefy from 'buefy';
import 'vue-bricks/lib/vueBricks.css';
import VueBricks from 'vue-bricks';
import Vue from 'vue';
import App from './App.vue';

Vue.config.productionTip = false;
Vue.use(Buefy);
Vue.use(VueBricks);

new Vue({
  render: h => h(App),
}).$mount('#app');
