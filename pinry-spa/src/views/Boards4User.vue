<template>
  <div class="boards-for-user">
    <PHeader></PHeader>
    <Boards :boardUsername="username"></Boards>
  </div>
</template>

<script>
import PHeader from '../components/PHeader.vue';
import Boards from '../components/Boards.vue';

export default {
  name: 'Boards4User',
  data() {
    return {
      username: null,
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
    this.initialize();
    next();
  },
  methods: {
    initialize() {
      this.username = this.$route.params.username;
    },
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">
</style>
