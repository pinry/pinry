import Vue from 'vue';
import VueRouter from 'vue-router';
import Home from '../views/Home.vue';
import Pins4Tag from '../views/Pins4Tag.vue';
import Pins4User from '../views/Pins4User.vue';
import Pins4Board from '../views/Pins4Board.vue';

Vue.use(VueRouter);

const routes = [
  {
    path: '/',
    name: 'home',
    component: Home,
  },
  {
    path: '/pins/tags/:tag',
    name: 'tag',
    component: Pins4Tag,
  },
  {
    path: '/pins/users/:user',
    name: 'user',
    component: Pins4User,
  },
  {
    path: '/pins/boards/:boardId',
    name: 'board',
    component: Pins4Board,
  },
];

const router = new VueRouter({
  routes,
});

export default router;
