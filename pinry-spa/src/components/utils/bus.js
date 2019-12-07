import Vue from 'vue';

const eventBus = new Vue();

export default {
  bus: eventBus,
  events: {
    refreshPin: 'refreshPin',
    refreshBoards: 'refreshBoards',
  },
};
