<template>
  <div id="app">
    <router-view/>
  </div>
</template>

<script>
export default {
  name: 'app',
};
</script>

<style lang="scss">
  // Import Bulma's core
  @import "~bulma/sass/utilities/_all";
  // Import Bulma and Buefy styles
  @import "~bulma";
  @import "~buefy/src/scss/buefy";
  html {
    background-color: #F5F5EB;
  }
  .body {
    font-family: 'Open Sans', sans-serif;
  }
</style>
