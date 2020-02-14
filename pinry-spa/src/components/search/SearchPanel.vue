<template>
  <div class="search-panel">
    <div class="filter-selector">
      <div class="card-content">
        <b-field>
          <b-select placeholder="Choose Filter" v-model="filterType">
            <option>Tag</option>
            <option>Board</option>
          </b-select>
          <b-autocomplete
            v-show="filterType === 'Tag'"
            class="search-input"
            v-model="name"
            :data="filteredDataArray"
            :keep-first="true"
            :open-on-focus="true"
            placeholder="select a filter then type to filter"
            icon="magnify"
            @select="option => selected = option">
            <template slot="empty">No results found</template>
          </b-autocomplete>
          <template v-if="filterType === 'Board'">
            <b-input
              class="search-input"
              type="search"
              v-model="boardText"
              placeholder="type to search board"
              icon="magnify"
            >
            </b-input>
            <p class="control">
              <b-button @click="searchBoard" class="button is-primary">Search</b-button>
            </p>
          </template>
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
      },
      name: '',
      boardText: '',
      selected: null,
    };
  },
  methods: {
    selectOption(filterName) {
      this.name = '';
      this.boardText = '';
      if (filterName === 'Tag') {
        this.selectedOption = this.options.Tag;
      }
    },
    searchBoard() {
      if (this.boardText === '') {
        return;
      }
      this.$emit(
        'selected',
        { filterType: this.filterType, selected: this.boardText },
      );
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
