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
  // Import Bulma and Buefy styles
  @use "bulma";
  @use "buefy/dist/buefy";
  html {
    background-color: #F5F5EB;
  }
  .body {
    font-family: 'Open Sans', sans-serif;
  }
</style>
