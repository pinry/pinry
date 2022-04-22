<template>
  <div class="search-panel">
    <div class="filter-selector">
      <div class="card-content">
        <b-field>
          <b-select v-bind:placeholder="$t('chooseFilterPlaceholder')" v-model="filterType">
            <option value="Tag">{{ $t("SearchPanelTagOption") }}</option>
            <option value="Board">{{ $t("SearchPanelBoardOption") }}</option>
          </b-select>
          <b-autocomplete
            v-show="filterType === 'Tag'"
            class="search-input"
            v-model="name"
            :data="filteredDataArray"
            :keep-first="true"
            :open-on-focus="true"
            v-bind:placeholder="$t('selectFilterPlaceholder')"
            icon="magnify"
            @select="option => selected = option">
            <template slot="empty">{{ $t("noResultsFound") }}</template>
          </b-autocomplete>
          <template v-if="filterType === 'Board'">
            <b-input
              class="search-input"
              type="search"
              v-model="boardText"
              v-bind:placeholder="$t('searchBoardPlaceholder')"
              icon="magnify"
            >
            </b-input>
            <p class="control">
              <b-button @click="searchBoard" class="button is-primary">{{ $t("searchButton") }}</b-button>
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
