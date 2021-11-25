<template>
  <div class="search-panel">
    <div class="filter-selector">
      <div class="card-content">
        <b-field>
          <b-select placeholder="Choose Filter" v-model="filterType">
            <option>Tag</option>
            <option>Board</option>
          </b-select>
          <b-taginput
            v-show="filterType === 'Tag'"
            v-model="name"
            :data="filteredTags"
            autocomplete
            :open-on-focus="true"
            icon="magnify"
            placeholder="select a filter then type to filter"
            @input="option => selected = option"
            @typing="filterTags">
            <template slot="empty">No results found</template>
            </b-taginput>
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
      filteredTags: [],
      options: {
        Tag: [],
      },
      name: [],
      boardText: '',
      selected: null,
    };
  },
  methods: {
    selectOption(filterName) {
      this.name = [];
      this.boardText = '';
      if (filterName === 'Tag') {
        this.filteredTags = this.options.Tag;
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
    filterTags(text) {
      this.filteredTags = this.options.Tag.filter(tag => tag.toLowerCase().includes(text.toLowerCase()));
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
