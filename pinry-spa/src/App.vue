<template>
  <div id="app">
    <router-view />
  </div>
</template>

<script>
export default {
  name: 'App',
};
</script>

<style lang="scss">
  html {
    background-color: var(--pinry-page-background);
  }
  .body {
    font-family: 'Open Sans', sans-serif;
  }
</style>
