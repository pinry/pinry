<template>
  <div class="pins-for-board">
    <PHeader></PHeader>
    <Pins :pin-filters="filters"></Pins>
  </div>
</template>

<script>
import PHeader from '../components/PHeader.vue';
import Pins from '../components/Pins.vue';

export default {
  name: 'Pins4Board',
  data() {
    return {
      filters: { boardFilter: null },
    };
  },
  components: {
    PHeader,
    Pins,
  },
  beforeRouteUpdate(to, from, next) {
    this.filters = { boardFilter: to.params.boardId };
    next();
  },
  created() {
    this.initializeBoard();
  },
  methods: {
    initializeBoard() {
      this.filters = { boardFilter: this.$route.params.boardId };
    },
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">
</style>
