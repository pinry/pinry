<template>
  <div class="pin-create-modal">
    <div>
      <div class="modal-card" style="width: auto">
        <header class="modal-card-head">
          <p class="modal-card-title">{{ editorMeta.title }}</p>
        </header>
        <section class="modal-card-body">
          <div class="columns">
            <div class="column">
              <FileUpload
                :previewImageURL="pinModel.form.url.value"
                v-on:imageUploadSucceed="onUploadDone"
                v-on:imageUploadProcessing="onUploadProcessing"
              ></FileUpload>
            </div>
            <div class="column">
              <b-field label="Image URL"
                       v-show="!disableUrlField && !isEdit"
                       :type="pinModel.form.url.type"
                       :message="pinModel.form.url.error">
                <b-input
                  type="text"
                  v-model="pinModel.form.url.value"
                  placeholder="where to fetch the image"
                  maxlength="256"
                >
                </b-input>
              </b-field>
              <b-field label="Privacy Option"
                       :type="pinModel.form.private.type"
                       :message="pinModel.form.private.error">
                <b-checkbox v-model="pinModel.form.private.value">
                    {{ pinModel.form.private.value?"only visible to yourself":"visible to everyone" }}
                </b-checkbox>
              </b-field>
              <b-field label="Image Referer"
                       :type="pinModel.form.referer.type"
                       :message="pinModel.form.referer.error">
                <b-input
                  type="text"
                  v-model="pinModel.form.referer.value"
                  placeholder="where to find the pin"
                  maxlength="256"
                >
                </b-input>
              </b-field>
              <b-field label="Tags">
                <b-taginput
                    v-model="pinModel.form.tags.value"
                    :data="editorMeta.filteredTagOptions"
                    autocomplete
                    ellipsis
                    icon="label"
                    :allow-new="true"
                    placeholder="Add a tag"
                    @typing="getFilteredTags">
                  <template slot-scope="props">
                    <strong>{{ props.option }}</strong>
                  </template>
                  <template slot="empty">
                    There are no items
                  </template>
                </b-taginput>
              </b-field>
              <b-field label="Descripton"
                       :type="pinModel.form.description.type"
                       :message="pinModel.form.description.error">
                <b-input
                  type="textarea"
                  v-model="pinModel.form.description.value"
                  placeholder="idea from this pin"
                  maxlength="1024"
                >
                </b-input>
              </b-field>
            </div>
            <div class="column" v-if="!isEdit">
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
            v-if="!isEdit"
            @click="createPin"
            class="button is-primary">Create Pin
          </button>
          <button
            v-if="isEdit"
            @click="savePin"
            class="button is-primary">Save Changes
          </button>
        </footer>
      </div>
    </div>
  </div>
</template>

<script>
import API from '../api';
import FileUpload from './FileUpload.vue';
import FilterSelect from './FilterSelect.vue';
import bus from '../utils/bus';
import ModelForm from '../utils/ModelForm';
import Loading from '../utils/Loading';
import AutoComplete from '../utils/AutoComplete';

function isURLBlank(url) {
  return url !== null && url === '';
}

const fields = ['url', 'referer', 'description', 'tags', 'private'];

export default {
  name: 'PinCreateModal',
  props: {
    fromUrl: {
      type: Object,
      default: null,
    },
    username: {
      type: String,
      default: null,
    },
    isEdit: {
      type: Boolean,
      default: false,
    },
    existedPin: {
      type: Object,
      default: null,
    },
  },
  components: {
    FileUpload,
    FilterSelect,
  },
  data() {
    const pinModel = ModelForm.fromFields(fields);
    pinModel.form.tags.value = [];
    return {
      disableUrlField: false,
      pinModel,
      formUpload: {
        imageId: null,
      },
      boardId: null,
      boardOptions: [],
      tagOptions: [],
      editorMeta: {
        title: 'New Pin',
        filteredTagOptions: [],
      },
    };
  },
  created() {
    this.fetchBoardList();
    this.fetchTagList();
    if (this.isEdit) {
      this.editorMeta.title = 'Edit Pin';
      this.pinModel.form.url.value = this.existedPin.url;
      this.pinModel.form.referer.value = this.existedPin.referer;
      this.pinModel.form.description.value = this.existedPin.description;
      this.pinModel.form.tags.value = this.existedPin.tags;
      this.pinModel.form.private.value = this.existedPin.private;
    } else {
      this.pinModel.form.private.value = false;
    }
    if (this.fromUrl) {
      this.pinModel.form.url.value = this.fromUrl.url;
      this.pinModel.form.referer.value = this.fromUrl.referer;
      this.pinModel.form.description.value = this.fromUrl.description;
    }
  },
  methods: {
    fetchTagList() {
      API.Tag.fetchList().then(
        (resp) => {
          this.tagOptions = resp.data;
        },
      );
    },
    getFilteredTags(text) {
      const filteredTagOptions = [];
      AutoComplete.getFilteredOptions(
        this.tagOptions,
        text,
      ).forEach(
        (option) => {
          filteredTagOptions.push(option.name);
        },
      );
      this.editorMeta.filteredTagOptions = filteredTagOptions;
    },
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
    savePin() {
      const self = this;
      const data = this.pinModel.asDataByFields(
        ['referer', 'description', 'tags', 'private'],
      );
      const promise = API.Pin.updateById(this.existedPin.id, data);
      promise.then(
        (resp) => {
          bus.bus.$emit(bus.events.refreshPin);
          self.$emit('pinUpdated', resp);
          self.$parent.close();
        },
      );
    },
    createPin() {
      const loading = Loading.open(this);
      const self = this;
      let promise;
      if (isURLBlank(this.pinModel.form.url.value) && this.formUpload.imageId === null) {
        return;
      }
      if (this.formUpload.imageId === null) {
        const data = this.pinModel.asDataByFields(fields);
        promise = API.Pin.createFromURL(data);
      } else {
        const data = this.pinModel.asDataByFields(
          ['referer', 'description', 'tags', 'private'],
        );
        data.image_by_id = this.formUpload.imageId;
        promise = API.Pin.createFromUploaded(data);
      }
      promise.then(
        (resp) => {
          bus.bus.$emit(bus.events.refreshPin);
          self.$emit('pinCreated', resp);
          self.$parent.close();
          loading.close();
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
