<template>
  <div class="pins-for-tag">
    <PHeader></PHeader>
    <Pins :pin-filters="filters"></Pins>
  </div>
</template>

<script>
import PHeader from '../components/PHeader.vue';
import Pins from '../components/Pins.vue';

export default {
  name: 'Pins4Id',
  data() {
    return {
      filters: { idFilter: null },
    };
  },
  components: {
    PHeader,
    Pins,
  },
  created() {
    this.initialize();
  },
  beforeRouteUpdate(to, from, next) {
    this.filters = { idFilter: to.params.pinId };
    next();
  },
  methods: {
    initialize() {
      this.filters = { idFilter: this.$route.params.pinId };
    },
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">
</style>
