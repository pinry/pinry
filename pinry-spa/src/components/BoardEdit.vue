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
import formUtils from './utils/form';

const fields = ['name'];

export default {
  name: 'BoardEditModal',
  data() {
    const model = formUtils.fromFields(fields);
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
          Object.entries(resp.data).forEach(
            (errorTuple) => {
              const [key, error] = errorTuple;
              let msg;
              if (Array.isArray(error)) {
                [msg] = error;
              } else {
                msg = error;
              }
              this.helper.markFieldAsDanger(key, msg);
            },
          );
        },
      );
    },
  },
};
</script>
