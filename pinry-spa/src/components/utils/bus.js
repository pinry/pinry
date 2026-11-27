import { createApp } from 'vue';

const eventBus = createApp({});

export default {
  bus: eventBus,
  events: {
    refreshPin: 'refreshPin',
    refreshBoards: 'refreshBoards',
  },
};
