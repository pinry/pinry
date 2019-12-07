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
              <FileUpload
                :previewImageURL="createModel.form.url.value"
                v-on:imageUploadSucceed="onUploadDone"
                v-on:imageUploadProcessing="onUploadProcessing"
              ></FileUpload>
            </div>
            <div class="column">
              <b-field label="Image URL"
                       v-show="!disableUrlField"
                       :type="createModel.form.url.type"
                       :message="createModel.form.url.error">
                <b-input
                  type="text"
                  v-model="createModel.form.url.value"
                  placeholder="where to fetch the image"
                  maxlength="256"
                >
                </b-input>
              </b-field>
              <b-field label="Image Referer"
                       :type="createModel.form.referer.type"
                       :message="createModel.form.referer.error">
                <b-input
                  type="text"
                  v-model="createModel.form.referer.value"
                  placeholder="where to find the pin"
                  maxlength="256"
                >
                </b-input>
              </b-field>
              <b-field label="Descripton"
                       :type="createModel.form.description.type"
                       :message="createModel.form.description.error">
                <b-input
                  type="textarea"
                  v-model="createModel.form.description.value"
                  placeholder="idea from this pin"
                  maxlength="1024"
                >
                </b-input>
              </b-field>
              <b-field label="Tags">
                <b-taginput
                  v-model="createModel.form.tags.value"
                  ellipsis
                  icon="label"
                  placeholder="Add a tag">
                </b-taginput>
              </b-field>
            </div>
            <div class="column">
              <FilterSelect
                :allOptions="boardOptions"
                v-on:selected="onSelectBoard"
              ></FilterSelect>
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
import API from '../api';
import FileUpload from './FileUpload.vue';
import FilterSelect from './FilterSelect.vue';
import bus from '../utils/bus';
import ModelForm from '../utils/ModelForm';

function isURLBlank(url) {
  return url !== null && url !== '';
}

const fields = ['url', 'referer', 'description', 'tags'];

export default {
  name: 'PinCreateModal',
  props: ['username'],
  components: {
    FileUpload,
    FilterSelect,
  },
  data() {
    const createModel = ModelForm.fromFields(fields);
    createModel.form.tags.value = [];
    return {
      disableUrlField: false,
      createModel,
      formUpload: {
        imageId: null,
      },
      boardId: null,
      boardOptions: [],
    };
  },
  created() {
    this.fetchBoardList();
  },
  methods: {
    fetchBoardList() {
      API.Board.fetchFullList(this.username).then(
        (resp) => {
          const boardOptions = [];
          resp.data.forEach(
            (board) => {
              const boardOption = { name: board.name, value: board.id };
              boardOptions.push(boardOption);
            },
          );
          this.boardOptions = boardOptions;
        },
        () => {
          console.log('Error occurs while fetch board full list');
        },
      );
    },
    onSelectBoard(boardIds) {
      this.boardIds = boardIds;
    },
    onUploadProcessing() {
      this.disableUrlField = true;
    },
    onUploadDone(imageId) {
      this.formUpload.imageId = imageId;
    },
    createPin() {
      const self = this;
      let promise;
      if (isURLBlank(this.createModel.form.url.value) && this.formUpload.imageId === null) {
        return;
      }
      if (this.formUpload.imageId === null) {
        const data = this.createModel.asDataByFields(fields);
        promise = API.Pin.createFromURL(data);
      } else {
        const data = this.createModel.asDataByFields(
          ['referer', 'description', 'tags'],
        );
        data.image_by_id = this.formUpload.imageId;
        promise = API.Pin.createFromUploaded(data);
      }
      promise.then(
        (resp) => {
          bus.bus.$emit(bus.events.refreshPin);
          self.$emit('pinCreated', resp);
          self.$parent.close();
          if (self.boardIds !== null) {
            // FIXME(winkidney): Should handle error for add-to board
            self.boardIds.forEach(
              (boardId) => {
                API.Board.addToBoard(boardId, [resp.data.id]);
              },
            );
          }
        },
      );
    },
  },
};
</script>
