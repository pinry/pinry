<template>
  <div class="board-modal">
    <form action="">
      <div class="modal-card" style="width: auto">
        <header class="modal-card-head">
          <p class="modal-card-title">{{ UIMeta.title }}</p>
        </header>
        <section class="modal-card-body">
          <div v-if="!isEdit">
            <b-field label="Name"
                       :type="createModel.form.name.type"
                       :message="createModel.form.name.error">
                <b-input
                  type="text"
                  v-model="createModel.form.name.value"
                  placeholder="board name"
                  maxlength="128"
                  >
                </b-input>
              </b-field>
          </div>
          <div v-if="isEdit">
            <b-field label="Name"
                       :type="editModel.form.name.type"
                       :message="editModel.form.name.error">
                <b-input
                  type="text"
                  v-model="editModel.form.name.value"
                  placeholder="board name"
                  maxlength="128"
                  >
                </b-input>
              </b-field>
          </div>
        </section>
        <footer class="modal-card-foot">
          <button class="button" type="button" @click="$parent.close()">Close</button>
          <button
            v-if="!isEdit"
            @click="createBoard"
            class="button is-primary">Create Board
          </button>
          <button
            v-if="isEdit"
            @click="saveBoardChanges"
            class="button is-primary">Save Changes
          </button>
        </footer>
      </div>
    </form>
  </div>
</template>

<script>
import API from './api';
import ModelForm from './utils/ModelForm';

const fields = ['name'];

export default {
  name: 'BoardEditModal',
  data() {
    const createModel = ModelForm.fromFields(fields);
    const editModel = ModelForm.fromFields(fields);
    return {
      UIMeta: {
        title: 'Board Create',
      },
      createModel,
      editModel,
    };
  },
  props: {
    isEdit: {
      type: Boolean,
      default: false,
    },
    board: {
      type: Object,
      default() {
        return {};
      },
    },
  },
  created() {
    if (this.isEdit) {
      this.UIMeta.title = 'Board Edit';
      this.editModel.assignToForm(this.board);
    }
  },
  methods: {
    saveBoardChanges() {
      const self = this;
      const promise = API.Board.saveChanges(
        this.board.id,
        this.editModel.asData(),
      );
      promise.then(
        (resp) => {
          self.$emit('boardSaved', resp);
          self.$parent.close();
        },
        (resp) => {
          self.editModel.markFieldsAsDanger(resp.data);
        },
      );
    },
    createBoard() {
      const self = this;
      const promise = API.Board.create(this.createModel.form.name.value);
      promise.then(
        (resp) => {
          self.$emit('boardCreated', resp);
          self.$parent.close();
        },
        (resp) => {
          self.createModel.markFieldsAsDanger(resp.data);
        },
      );
    },
  },
};
</script>
