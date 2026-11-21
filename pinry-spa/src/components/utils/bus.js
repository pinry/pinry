import mitt from 'mitt';

const eventBus = mitt();

export default {
  bus: eventBus,
  events: {
    refreshPin: 'refreshPin',
    refreshBoards: 'refreshBoards',
  },
};
