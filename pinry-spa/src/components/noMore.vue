<template>
  <div v-show="show">
    <div id="the-end">&mdash; End &mdash;</div>
  </div>
</template>

<script>
export default {
  name: 'noMore',
  props: {
    show: {
      type: Boolean,
      default: false,
    },
  },
};
</script>

<style lang="scss" scoped>
#the-end {
    font-family: 'Georgia', 'Times', 'Times New Roman', serif;
    font-size: 1.4em;
    font-style: italic;
    text-align: center;
    padding: 50px;
}
</style>
