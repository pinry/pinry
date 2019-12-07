<template>
  <div class="editor">
    <div class="editor-buttons">
      <span class="icon-container" @click="deleteBoard">
         <b-icon
           type="is-light"
           icon="delete"
           custom-size="mdi-24px">
         </b-icon>
      </span>
      <span class="icon-container" @click="editBoard">
       <b-icon
         type="is-light"
         icon="pencil"
         custom-size="mdi-24px">
       </b-icon>
      </span>
    </div>
  </div>
</template>

<script>
import API from '../api';
import modals from '../modals';


export default {
  name: 'BoardEditor',
  props: {
    board: {
      default() {
        return {};
      },
      type: Object,
    },
  },
  methods: {
    onBoardSaved() {
      this.$emit('board-save-succeed');
    },
    editBoard() {
      modals.openBoardEdit(
        this,
        this.board,
        this.onBoardSaved,
      );
    },
    deleteBoard() {
      this.$buefy.dialog.confirm({
        message: 'Delete this Board?',
        onConfirm: () => {
          API.Board.delete(this.board.id).then(
            () => {
              this.$buefy.toast.open('Board deleted');
              this.$emit('board-delete-succeed', this.board.id);
            },
            () => {
              this.$buefy.toast.open(
                { type: 'is-danger', message: 'Failed to delete Board' },
              );
            },
          );
        },
      });
    },
  },
};
</script>

<style lang="scss" scoped>
@import './editor';
</style>
