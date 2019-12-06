<template>
  <div class="filter-select">
    <b-field label="Select Board"
             :type="form.name.type"
             :message="form.name.error">
      <b-input
        type="text"
        v-model="form.name.value"
        placeholder="Type to filter or Create one"
        maxlength="128"
      >
      </b-input>
    </b-field>
    <b-field>
      <button
        @click="createNewBoard"
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
import API from '../api';
import ModelForm from '../utils/ModelForm';

const fields = ['name'];

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

function getBoardFromResp(boardObject) {
  return { name: boardObject.name, value: boardObject.id };
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
      createdOptions: [],
    };
  },
  methods: {
    select(board) {
      this.selectedOptions = [board.value];
    },
    createNewBoard() {
      const self = this;
      const promise = API.Board.create(this.form.name.value);
      promise.then(
        (data) => {
          self.$emit('boardCreated', data);
          const board = getBoardFromResp(data);
          self.createdOptions.unshift(board);
          self.select(board);
          self.form.name.value = null;
        },
        (resp) => {
          self.helper.markFieldsAsDanger(resp.data);
        },
      );
    },
  },
  watch: {
    // eslint-disable-next-line func-names
    'form.name.value': function (newVal) {
      let availableOptions;
      if (newVal === '' || newVal === null) {
        availableOptions = this.allOptions;
      } else {
        availableOptions = getFilteredOptions(
          this.allOptions, this.form.name.value,
        );
      }
      this.availableOptions = this.createdOptions.concat(availableOptions);
    },
    createdOptions() {
      this.availableOptions = this.createdOptions.concat(this.availableOptions);
    },
    allOptions() {
      this.availableOptions = this.allOptions;
    },
    selectedOptions() {
      this.helper.resetAllFields();
      this.$emit('selected', this.selectedOptions);
    },
  },
};
</script>
