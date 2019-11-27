<template>
  <div class="home">
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
    this.initializeTag();
    next();
  },
  methods: {
    initializeTag() {
      this.filters.tagFilter = this.$route.params.tag;
    },
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">
</style>
