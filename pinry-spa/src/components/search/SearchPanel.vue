<template>
  <div class="search-panel">
    <div class="filter-selector">
      <div class="card-content">
        <b-field>
          <b-select v-bind:placeholder="$t('chooseFilterPlaceholder')" v-model="filterType">
            <option value="Tag">{{ $t("SearchPanelTagOption") }}</option>
            <option value="Board">{{ $t("SearchPanelBoardOption") }}</option>
          </b-select>
          <b-taginput
            v-show="filterType === 'Tag'"
            class="search-input"
            v-model="tags"
            :data="filteredTags"
            autocomplete
            :keep-first="true"
            :open-on-focus="true"
            v-bind:placeholder="$t('selectFilterPlaceholder')"
            icon="magnify"
            @typing="text => tagText = text">
            <template #empty>{{ $t("noResultsFound") }}</template>
          </b-taginput>
          <b-select v-show="filterType === 'Tag'" v-model="tagsMode">
            <option value="all">{{ $t("SearchPanelTagsModeAllOption") }}</option>
            <option value="any">{{ $t("SearchPanelTagsModeAnyOption") }}</option>
          </b-select>
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
  emits: ['selected'],
  data() {
    return {
      filterType: null,
      options: {
        Tag: [],
      },
      tags: [],
      tagText: '',
      tagsMode: 'all',
      boardText: '',
    };
  },
  methods: {
    selectOption() {
      this.tags = [];
      this.tagText = '';
      this.boardText = '';
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
    searchTags() {
      if (this.filterType !== 'Tag') {
        return;
      }
      this.$emit(
        'selected',
        { filterType: this.filterType, selected: this.tags, tagsMode: this.tagsMode },
      );
    },
  },
  watch: {
    filterType() {
      this.selectOption();
    },
    tags() {
      // b-taginput clears its input after adding a tag without emitting "typing"
      this.tagText = '';
      this.searchTags();
    },
    tagsMode() {
      if (this.tags.length > 0) {
        this.searchTags();
      }
    },
  },
  computed: {
    filteredTags() {
      const text = this.tagText.toLowerCase();
      return this.options.Tag.filter(
        tag => !this.tags.includes(tag) && tag.toLowerCase().indexOf(text) >= 0,
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
    background-color: var(--pinry-card-background);
    border-radius: 3px;
    .search-input {
      width: 100%;
    }
  }
</style>
