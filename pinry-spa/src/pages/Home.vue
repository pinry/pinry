<template>
  <div class="hello">
    <PHeader></PHeader>
    <section class="section">
      <div class="container">
      </div>
    </section>
  </div>
</template>

<script>
import PHeader from '../components/PHeader.vue';

export default {
  name: 'p-header',
  components: {
    PHeader,
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">
</style>
