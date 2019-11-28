<template>
  <div class="loading-spinner">
    <div v-show="show" class="spinner">
    </div>
  </div>
</template>

<script>
export default {
  name: 'loadingSpinner',
  props: {
    show: {
      type: Boolean,
      default: false,
    },
  },
};
</script>

<style lang="scss" scoped>
/* loading spinner */
.spinner {
    background: url('../assets/loader.gif');
    background-position: center center;
    background-repeat: no-repeat;
    height: 31px;
    margin: 0 auto;
    padding: 50px;
    width: 31px;
}
</style>
