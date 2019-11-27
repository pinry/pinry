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
      filters: { userFilter: null },
    };
  },
  components: {
    PHeader,
    Pins,
  },
  created() {
    this.initializeUser();
  },
  beforeRouteUpdate(to, from, next) {
    this.initializeUser();
    next();
  },
  methods: {
    initializeUser() {
      this.filters.userFilter = this.$route.params.user;
    },
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">
</style>
