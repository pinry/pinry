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
      <span class="icon-container">
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
export default {
  name: 'Editor',
  props: {
    show: {
      default: false,
      type: Boolean,
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
