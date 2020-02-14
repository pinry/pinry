<template>
  <div class="boards-for-user">
    <PHeader></PHeader>
    <Boards :filters="filters"></Boards>
  </div>
</template>

<script>
import PHeader from '../components/PHeader.vue';
import Boards from '../components/Boards.vue';

export default {
  name: 'Boards4User',
  data() {
    return {
      filters: { boardUsername: null },
    };
  },
  components: {
    PHeader,
    Boards,
  },
  created() {
    this.initialize();
  },
  beforeRouteUpdate(to, from, next) {
    this.filters = { boardUsername: to.params.username };
    next();
  },
  methods: {
    initialize() {
      this.filters = { boardUsername: this.$route.params.username };
    },
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">
</style>
