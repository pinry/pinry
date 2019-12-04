<template>
  <div class="image-upload">
    <div
      v-show="previewExists"
      class="has-text-centered is-center preview">
      <img :src="previewImageURL">
    </div>
    <div v-show="!previewExists">
      <b-field>
        <b-upload v-model="dropFiles"
                  multiple
                  drag-drop>
          <section class="section">
            <div class="content has-text-centered">
              <p>
                <b-icon
                  icon="upload"
                  size="is-medium">
                </b-icon>
              </p>
              <p>Drop your files here or click to upload</p>
            </div>
          </section>
        </b-upload>
      </b-field>
    </div>
  </div>
</template>

<script>
export default {
  name: 'FileUpload',
  props: {
    previewImageURL: {
      type: String,
      default: null,
    },
  },
  computed: {
    previewExists() {
      return this.previewImageURL !== null && this.previewImageURL !== '';
    },
  },
  data() {
    return {
      dropFiles: [],
    };
  },
  methods: {},
};
</script>

<style lang="scss" scoped>
@import '../utils/pin';
@import '../utils/loader';

.preview > img {
  width: $pin-preview-width;
  height: auto;
  @include loader('../../assets/loader.gif');
}

</style>
