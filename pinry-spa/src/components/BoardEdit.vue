<template>
  <div class="board-modal">
    <form action="">
      <div class="modal-card" style="width: auto">
        <header class="modal-card-head">
          <p class="modal-card-title">Board Create</p>
        </header>
        <section class="modal-card-body">
              <b-field label="Name"
                       :type="form.name.type"
                       :message="form.name.error">
                <b-input
                  type="text"
                  v-model="form.name.value"
                  placeholder="board name"
                  maxlength="128"
                  >
                </b-input>
              </b-field>
        </section>
        <footer class="modal-card-foot">
          <button class="button" type="button" @click="$parent.close()">Close</button>
          <button
            @click="createBoard"
            class="button is-primary">Create Board
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
    const model = ModelForm.fromFields(fields);
    return {
      form: model.form,
      helper: model,
    };
  },
  methods: {
    createBoard() {
      const self = this;
      const promise = API.Board.create(this.form.name.value);
      promise.then(
        (resp) => {
          self.$emit('boardCreated', resp);
          self.$parent.close();
        },
        (resp) => {
          self.helper.markFieldsAsDanger(resp.data);
        },
      );
    },
  },
};
</script>
