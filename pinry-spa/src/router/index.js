import Vue from 'vue';
import VueRouter from 'vue-router';
import Home from '../views/Home.vue';
import Pins4Tag from '../views/Pins4Tag.vue';
import Pins4User from '../views/Pins4User.vue';
import Pins4Board from '../views/Pins4Board.vue';
import Pins4Id from '../views/Pins4Id.vue';
import Boards4User from '../views/Boards4User.vue';
import Profile4User from '../views/Profile4User.vue';
import PinCreate from '../views/PinCreate.vue';
import Search from '../views/Search.vue';
import PageNotFound from '../views/PageNotFound.vue';

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
  {
    path: '/pins/:pinId',
    name: 'pin',
    component: Pins4Id,
  },
  {
    path: '/boards/users/:username',
    name: 'boards4user',
    component: Boards4User,
  },
  {
    path: '/profile/:username',
    name: 'profile4user',
    component: Profile4User,
  },
  {
    path: '/pin-creation/from-url',
    name: 'pin-creation-from-url',
    component: PinCreate,
  },
  {
    path: '/search',
    name: 'search',
    component: Search,
  },
  {
    path: '*',
    name: 'PageNotFound',
    component: PageNotFound,
  },
];

const router = new VueRouter({
  mode: 'history',
  routes,
});

export default router;
