<template>
  <div id="app">
    <Home></Home>
  </div>
</template>

<script>
import Home from './pages/Home.vue';

export default {
  name: 'app',
  components: {
    Home,
  },
};
</script>

<style lang="scss">
  // Import Bulma's core
  @import "~bulma/sass/utilities/_all";
  // Import Bulma and Buefy styles
  @import "~bulma";
  @import "~buefy/src/scss/buefy";
</style>
