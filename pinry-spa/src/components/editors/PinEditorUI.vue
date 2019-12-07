<template>
  <div class="editor">
    <div class="editor-buttons">
      <span class="icon-container">
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
      <span class="icon-container" @click="deletePin">
         <b-icon
           type="is-light"
           icon="delete"
           custom-size="mdi-24px">
         </b-icon>
      </span>
      <span class="icon-container">
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
    pin: {
      default() {
        return {};
      },
      type: Object,
    },
  },
  methods: {
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
