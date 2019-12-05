<template>
  <div class="filter-select">
    <b-field label="Select Board"
             :type="form.board.type"
             :message="form.board.error">
      <b-input
        type="text"
        v-model="form.board.value"
        placeholder="Type to filter or Create one"
        maxlength="128"
      >
      </b-input>
    </b-field>
    <b-field>
      <button
        class="button is-primary">
        Create New Board
      </button>
    </b-field>
    <b-field>
      <b-select
        class="select-list"
        multiple
        expanded
        native-size="8"
        v-model="selectedOptions">
        <template v-for="option in availableOptions">
          <option
            v-bind:key="option.value"
            :value="option.value">{{ option.name }}</option>
        </template>
      </b-select>
    </b-field>
  </div>
</template>

<script>
// import API from '../api';
import ModelForm from '../utils/ModelForm';

const fields = ['board'];

function getFilteredOptions(options, filterText) {
  return options.filter(
    (option) => {
      const index = option.name
        .toString()
        .toLowerCase()
        .indexOf(filterText.toLowerCase());
      return index >= 0;
    },
  );
}

export default {
  name: 'FilterSelect',
  props: {
    allOptions: {
      type: Array,
      default() {
        return [];
      },
    },
  },
  data() {
    const model = ModelForm.fromFields(fields);
    return {
      form: model.form,
      selectedOptions: [],
      helper: model,
      availableOptions: [],
    };
  },
  watch: {
    'form.board.value': function (newVal) {
      if (newVal === '' || newVal === null) {
        this.availableOptions = this.allOptions;
      } else {
        this.availableOptions = getFilteredOptions(
          this.allOptions, this.form.board.value,
        );
      }
    },
    allOptions() {
      this.availableOptions = this.allOptions;
    },
  },
};
</script>
