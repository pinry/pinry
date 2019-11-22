<template>
  <div class="hello">
    <PHeader></PHeader>
    <Pins></Pins>
  </div>
</template>

<script>
import PHeader from '../components/PHeader.vue';
import Pins from '../components/Pins.vue';

export default {
  name: 'p-header',
  components: {
    PHeader,
    Pins,
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">
</style>
