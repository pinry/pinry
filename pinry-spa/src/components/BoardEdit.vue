<template>
  <div class="board-modal">
    <div>
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
            <b-field label="Privacy Option"
                       :type="createModel.form.private.type"
                       :message="createModel.form.private.error">
                <b-checkbox v-model="createModel.form.private.value">
                    {{ createModel.form.private.value?"only visible to yourself":"visible to everyone" }}
                </b-checkbox>
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
            <b-field label="Privacy Option"
                       :type="editModel.form.private.type"
                       :message="editModel.form.private.error">
                <b-checkbox v-model="editModel.form.private.value">
                    {{ editModel.form.private.value?"only visible to yourself":"visible to everyone" }}
                </b-checkbox>
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
    </div>
  </div>
</template>

<script>
import API from './api';
import ModelForm from './utils/ModelForm';
import bus from './utils/bus';

const fields = ['name', 'private'];

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
    } else {
      this.createModel.form.private.value = false;
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
        (error) => {
          self.editModel.markFieldsAsDanger(error.response.data);
        },
      );
    },
    createBoard() {
      const self = this;
      const promise = API.Board.create(
        this.createModel.form.name.value,
        this.createModel.form.private.value,
      );
      promise.then(
        (resp) => {
          bus.bus.$emit(bus.events.refreshBoards);
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
