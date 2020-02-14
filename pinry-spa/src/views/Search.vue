<template>
  <div class="pins-for-tag">
    <PHeader></PHeader>
    <SearchPanel v-on:selected="doSearch"></SearchPanel>
    <Pins v-if="pinFilters" :pin-filters="pinFilters"></Pins>
    <Boards v-if="boardFilters" :filters="boardFilters"></Boards>
  </div>
</template>

<script>
import PHeader from '../components/PHeader.vue';
import Pins from '../components/Pins.vue';
import Boards from '../components/Boards.vue';
import SearchPanel from '../components/search/SearchPanel.vue';

export default {
  name: 'Search',
  data() {
    return {
      pinFilters: null,
      boardFilters: null,
    };
  },
  components: {
    PHeader,
    Pins,
    Boards,
    SearchPanel,
  },
  created() {},
  methods: {
    doSearch(args) {
      this.pinFilters = null;
      this.boardFilters = null;
      if (args.filterType === 'Tag') {
        this.pinFilters = { tagFilter: args.selected };
      } else if (args.filterType === 'Board') {
        this.boardFilters = { boardNameContains: args.selected };
      }
    },
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">
</style>
