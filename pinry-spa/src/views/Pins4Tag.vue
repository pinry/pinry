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
  name: 'Pins4Tag',
  data() {
    return {
      filters: { tagFilter: null },
    };
  },
  components: {
    PHeader,
    Pins,
  },
  created() {
    this.initializeTag();
  },
  beforeRouteUpdate(to, from, next) {
    this.filters = { tagFilter: to.params.tag };
    next();
  },
  methods: {
    initializeTag() {
      this.filters = { tagFilter: this.$route.params.tag };
    },
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">
</style>
