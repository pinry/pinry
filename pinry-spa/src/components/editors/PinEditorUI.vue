<template>
  <div class="editor">
    <div class="editor-buttons">
      <span class="icon-container" v-if="inBoard" @click="removeFromBoard">
          <b-icon
            type="is-light"
            icon="minus-box"
            custom-size="mdi-24px">
         </b-icon>
      </span>
      <span class="icon-container">
          <b-icon
            type="is-light"
            icon="plus-box"
            custom-size="mdi-24px">
         </b-icon>
      </span>
      <span class="icon-container" @click="deletePin" v-if="isOwner">
         <b-icon
           type="is-light"
           icon="delete"
           custom-size="mdi-24px">
         </b-icon>
      </span>
      <span class="icon-container" v-if="isOwner">
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

export default {
  name: 'Editor',
  props: {
    currentBoardId: {
      type: Number,
      default: null,
    },
    currentUsername: {
      default: '',
      type: String,
    },
    pin: {
      default() {
        return {};
      },
      type: Object,
    },
  },
  computed: {
    isOwner() {
      return this.pin.author === this.currentUsername;
    },
    inBoard() {
      return this.currentBoardId !== null;
    },
  },
  methods: {
    removeFromBoard() {
      this.$buefy.dialog.confirm({
        message: 'Remove Pin from Board?',
        onConfirm: () => {
          API.Board.removeFromBoard(this.currentBoardId, [this.pin.id]).then(
            () => {
              this.$buefy.toast.open('Pin removed');
              this.$emit('pin-remove-from-board-succeed', this.pin.id);
            },
            () => {
              this.$buefy.toast.open(
                { type: 'is-danger', message: 'Failed to Remove Pin' },
              );
            },
          );
        },
      });
    },
    deletePin() {
      this.$buefy.dialog.confirm({
        message: 'Delete this Pin?',
        onConfirm: () => {
          API.Pin.deleteById(this.pin.id).then(
            () => {
              this.$buefy.toast.open('Pin deleted');
              this.$emit('pin-delete-succeed', this.pin.id);
            },
            () => {
              this.$buefy.toast.open(
                { type: 'is-danger', message: 'Failed to delete Pin' },
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
