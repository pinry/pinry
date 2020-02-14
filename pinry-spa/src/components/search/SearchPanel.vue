<template>
  <div class="search-panel">
    <div class="filter-selector">
      <div class="card-content">
        <b-field>
          <b-select placeholder="Filter Type" v-model="filterType">
            <option>Tag</option>
            <option>Board</option>
          </b-select>
          <b-autocomplete
            class="search-input"
            v-model="name"
            :data="filteredDataArray"
            :keep-first="false"
            :open-on-focus="true"
            placeholder="select a filter then type to filter"
            icon="magnify"
            @select="option => selected = option">
            <template slot="empty">No results found</template>
          </b-autocomplete>
        </b-field>
      </div>
    </div>
  </div>
</template>

<script>
import api from '../api';

export default {
  name: 'FilterSelector',
  data() {
    return {
      filterType: null,
      selectedOption: [],
      options: {
        Tag: [],
        Board: [],
      },
      name: '',
      selected: null,
    };
  },
  methods: {
    selectOption(filterName) {
      if (filterName === 'Tag') {
        this.selectedOption = this.options.Tag;
      } else {
        this.selectedOption = this.options.Board;
      }
    },
  },
  watch: {
    filterType(newVal) {
      this.selectOption(newVal);
    },
    selected(newVal) {
      this.$emit(
        'selected',
        { filterType: this.filterType, selected: newVal },
      );
    },
  },
  computed: {
    filteredDataArray() {
      return this.selectedOption.filter(
        (option) => {
          const ret = option
            .toString()
            .toLowerCase()
            .indexOf(this.name.toLowerCase()) >= 0;
          return ret;
        },
      );
    },
  },
  created() {
    api.Board.fetchSiteFullList().then(
      (resp) => {
        const options = [];
        resp.data.forEach(
          (board) => {
            options.push(board.name);
          },
        );
        this.options.Board = options;
      },
    );
    api.Tag.fetchList().then(
      (resp) => {
        const options = [];
        resp.data.forEach(
          (tag) => {
            options.push(tag.name);
          },
        );
        this.options.Tag = options;
      },
    );
  },
};
</script>

<style scoped="scoped" lang="scss">
  .search-panel {
    padding-top: 3rem;
    padding-left: 2rem;
    padding-right: 2rem;
  }
  .filter-selector {
    background-color: white;
    border-radius: 3px;
    .search-input {
      width: 100%;
    }
  }
</style>
