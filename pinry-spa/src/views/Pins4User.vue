<template>
  <div class="pins-for-user">
    <PHeader></PHeader>
    <UserProfileCard :in-pins="true" :username="filters.userFilter"></UserProfileCard>
    <Pins :pin-filters="filters"></Pins>
  </div>
</template>

<script>
import PHeader from '../components/PHeader.vue';
import UserProfileCard from '../components/UserProfileCard.vue';
import Pins from '../components/Pins.vue';

export default {
  name: 'Pins4User',
  data() {
    return {
      filters: { userFilter: null },
    };
  },
  components: {
    PHeader,
    UserProfileCard,
    Pins,
  },
  created() {
    this.initializeBoard();
  },
  beforeRouteUpdate(to, from, next) {
    this.filters = { userFilter: to.params.user };
    next();
  },
  methods: {
    initializeBoard() {
      this.filters = { userFilter: this.$route.params.user };
    },
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">
</style>
