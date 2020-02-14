<template>
  <div class="pins-for-tag">
    <PHeader></PHeader>
    <SearchPanel v-on:selected="doSearch"></SearchPanel>
    <Pins v-if="filters" :pin-filters="filters"></Pins>
    <Pins v-if="filters" :pin-filters="filters"></Pins>
  </div>
</template>

<script>
import PHeader from '../components/PHeader.vue';
import Pins from '../components/Pins.vue';
import SearchPanel from '../components/search/SearchPanel.vue';

export default {
  name: 'Search',
  data() {
    return {
      filters: null,
    };
  },
  components: {
    PHeader,
    Pins,
    SearchPanel,
  },
  created() {},
  methods: {
    doSearch(args) {
      this.filters = null;
      if (args.filterType === 'Tag') {
        this.filters = { tagFilter: args.selected };
      } else if (args.filter === 'Board') {
        this.filters = null;
      }
    },
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">
</style>
