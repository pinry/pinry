<template>
  <div class="pin-create-modal">
    <form action="">
      <div class="modal-card" style="width: auto">
        <header class="modal-card-head">
          <p class="modal-card-title">New Pin</p>
        </header>
        <section class="modal-card-body">
          <div class="columns">
            <div class="column">
              <FileUpload :previewImageURL="form.url.value"></FileUpload>
            </div>
            <div class="column">
              <b-field label="Image URL"
                       :type="form.url.type"
                       :message="form.url.error">
                <b-input
                  type="text"
                  v-model="form.url.value"
                  placeholder="where to fetch the image"
                  maxlength="256"
                  >
                </b-input>
              </b-field>
              <b-field label="Image Referer"
                       :type="form.referer.type"
                       :message="form.referer.error">
                <b-input
                  type="text"
                  v-model="form.referer.value"
                  placeholder="where to find the pin"
                  maxlength="256"
                  >
                </b-input>
              </b-field>
              <b-field label="Descripton"
                       :type="form.description.type"
                       :message="form.description.error">
                <b-input
                  type="textarea"
                  v-model="form.description.value"
                  placeholder="idea from this pin"
                  maxlength="1024"
                  >
                </b-input>
              </b-field>
              <b-field label="Tags">
                <b-taginput
                  v-model="form.tags.value"
                  ellipsis
                  icon="label"
                  placeholder="Add a tag">
                </b-taginput>
              </b-field>
            </div>
          </div>
        </section>
        <footer class="modal-card-foot">
          <button class="button" type="button" @click="$parent.close()">Close</button>
          <button
            @click="createPin"
            class="button is-primary">Create Pin
          </button>
        </footer>
      </div>
    </form>
  </div>
</template>

<script>
import api from '../api';
import FileUpload from './FileUpload.vue';

function isURLBlank(url) {
  return url !== null && url !== '';
}

export default {
  name: 'PinCreateModal',
  components: {
    FileUpload,
  },
  data() {
    return {
      form: {
        url: { value: null, error: null, type: null },
        referer: { value: null, error: null, type: null },
        description: { value: null, error: null, type: null },
        tags: { value: [], error: null, type: null },
      },
    };
  },
  methods: {
    createPin() {
      const self = this;
      if (isURLBlank(isURLBlank)) {
        const data = {
          url: this.form.url.value,
          referer: this.form.referer.value,
          description: this.form.description.value,
          tags: this.form.tags.value,
        };
        const promise = api.Pin.createFromURL(data);
        promise.then(
          (resp) => {
            self.$emit('pin.created', resp);
            self.$parent.close();
          },
        );
      }
    },
  },
};
</script>
