<template>
  <div class="home">
    <PHeader></PHeader>
    <Pins></Pins>
  </div>
</template>

<script>
import PHeader from '../components/PHeader.vue';
import Pins from '../components/Pins.vue';

export default {
  name: 'Home',
  components: {
    PHeader,
    Pins,
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">
</style>
