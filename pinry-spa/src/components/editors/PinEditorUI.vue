<template>
  <div class="editor">
    <div class="editor-buttons">
      <span class="icon-container">
          <b-icon
            type="is-light"
            icon="heart"
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
              this.$buefy.toast.open('Failed to delete Pin');
            },
          );
        },
      });
    },
  },
};
</script>

<style lang="scss" scoped>
@mixin border-radius {
  border-radius: 3px;
}

.editor-buttons {
  padding: 3px 1px 3px 3px;
  background-color: rgba(225, 225, 225, 0.6);
  position: absolute;
  top: 5px;
  right: 5px;
  float: right;
  cursor: pointer;

  @include border-radius;
  .icon-container {
    @include border-radius;
    padding: 5px 2px 2px 2px;
    background-color: rgba(0, 0, 0, 0.8);
    margin-right: 2px;
    span {
      opacity: 0.9;
    }
  }
}
</style>
