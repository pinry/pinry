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
  name: 'p-header',
  data() {
    return {
      filters: { boardFilter: null },
    };
  },
  components: {
    PHeader,
    Pins,
  },
  created() {
    this.initializeBoard();
  },
  beforeRouteUpdate(to, from, next) {
    this.initializeBoard();
    next();
  },
  methods: {
    initializeBoard() {
      this.filters.boardFilter = this.$route.params.boardId;
    },
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">
</style>
