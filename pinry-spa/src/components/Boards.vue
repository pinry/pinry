<template>
  <div class="boards">
    <section class="section">
      <div id="boards-container" class="container" v-if="blocks">
        <MasonryWall
          :items="blocks"
          :column-width="boardWidth"
          :gap="gutter"
          :key-mapper="itemKey"
        >
          <template #default="{ item }">
            <div :class="item.class"
                 class="grid">
              <div class="board-card grid-item">
                <div @mouseenter="currentEditBoard = item.id"
                     @mouseleave="currentEditBoard = null"
                >
                  <div class="card-image">
                    <BoardEditorUI
                      v-show="shouldShowEdit(item)"
                      :board="item"
                      v-on:board-delete-succeed="reset"
                      v-on:board-save-succeed="reset"
                    ></BoardEditorUI>
                    <router-link :to="{ name: 'board', params: { boardId: item.id } }">
                      <img :src="item.preview_image_url"
                         @load="onPinImageLoaded(item.id)"
                         :style="item.style"
                         v-show="item.preview_image_url"
                         class="preview-image">
                    </router-link>
                  </div>
                  <div class="board-footer">
                    <p class="sub-title board-info">{{ item.name }}</p>
                    <p class="description">
                      <small>
                        {{ $t("pinsInBoard") }}<span class="num-pins">{{ item.total_pins }}</span>
                      </small>
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </template>
        </MasonryWall>
      </div>
      <loadingSpinner v-bind:show="status.loading"></loadingSpinner>
      <noMore v-bind:show="!status.hasNext"></noMore>
    </section>
  </div>
</template>

<script>
import { MasonryWall } from '@yeger/vue-masonry-wall';
import API from './api';
import pinHandler from './utils/PinHandler';
import loadingSpinner from './loadingSpinner.vue';
import noMore from './noMore.vue';
import scroll from './utils/scroll';
import placeholder from '../assets/pinry-placeholder.jpg';
import BoardEditorUI from './editors/BoardEditUI.vue';
import bus from './utils/bus';

function createBoardItem(board) {
  const defaultPreviewImage = placeholder;
  const boardItem = {};
  let previewImage = {
    image: { thumbnail: { image: null, width: 240, height: 240 } },
  };
  if (board.cover !== null) {
    previewImage = board.cover;
  }
  boardItem.id = board.id;
  boardItem.name = board.name;
  boardItem.private = board.private;
  boardItem.total_pins = board.total_pins;
  if (previewImage.image.thumbnail.image !== null) {
    boardItem.preview_image_url = pinHandler.escapeUrl(
      previewImage.image.thumbnail.image,
    );
  } else {
    boardItem.preview_image_url = defaultPreviewImage;
  }
  boardItem.style = {
    width: `${previewImage.image.thumbnail.width}px`,
    height: `${previewImage.image.thumbnail.height}px`,
  };
  boardItem.class = {};
  boardItem.author = board.submitter.username;
  return boardItem;
}

function initialData() {
  return {
    boardWidth: 240,
    gutter: 15,
    currentEditBoard: null,
    blocks: [],
    blocksMap: {},
    status: {
      loading: false,
      hasNext: true,
      offset: 0,
    },
    editorMeta: {
      user: { loggedIn: false, meta: { username: null } },
    },
  };
}

export default {
  name: 'boards',
  components: {
    MasonryWall,
    loadingSpinner,
    noMore,
    BoardEditorUI,
  },
  data: initialData,
  props: ['filters'],
  watch: {
    filters() {
      this.reset();
    },
  },
  methods: {
    itemKey(item) {
      return item.id;
    },
    initialize() {
      this.initializeMeta();
      this.fetchMore(true);
    },
    initializeMeta() {
      const self = this;
      API.User.fetchUserInfo().then(
        (user) => {
          if (user === null) {
            self.editorMeta.user.loggedIn = false;
            self.editorMeta.user.meta = {};
          } else {
            self.editorMeta.user.meta = user;
            self.editorMeta.user.loggedIn = true;
          }
        },
      );
    },
    reset() {
      const data = initialData();
      Object.entries(data).forEach(
        (kv) => {
          const [key, value] = kv;
          this[key] = value;
        },
      );
      this.initialize();
    },
    shouldShowEdit(board) {
      if (!this.editorMeta.user.loggedIn) {
        return false;
      }
      if (this.editorMeta.user.meta.username !== board.author) {
        return false;
      }
      return this.currentEditBoard === board.id;
    },
    onPinImageLoaded(itemId) {
      this.blocksMap[itemId].class = {
        'image-loaded': true,
      };
      this.blocksMap[itemId].style.height = 'auto';
    },
    registerScrollEvent() {
      const self = this;
      this.unbindScroll = scroll.bindScroll2Bottom(
        () => {
          if (self.status.loading || !self.status.hasNext) {
            return;
          }
          self.fetchMore();
        },
      );
    },
    buildBlocks(results) {
      const blocks = [];
      results.forEach(
        (pin) => {
          const item = createBoardItem(pin);
          blocks.push(
            item,
          );
        },
      );
      return blocks;
    },
    shouldFetchMore(created) {
      if (!created) {
        if (this.status.loading) {
          return false;
        }
        if (!this.status.hasNext) {
          return false;
        }
      }
      return true;
    },
    fetchMore(created) {
      if (!this.shouldFetchMore(created)) {
        return;
      }
      let promise;
      if (this.filters.boardUsername) {
        promise = API.fetchBoardForUser(
          this.filters.boardUsername,
          this.status.offset,
        );
      } else if (this.filters.boardNameContains) {
        promise = API.Board.fetchListWhichContains(
          this.filters.boardNameContains,
          this.status.offset,
        );
      } else {
        return;
      }
      this.status.loading = true;
      promise.then(
        (resp) => {
          const { results, next } = resp.data;
          let newBlocks = this.buildBlocks(results);
          newBlocks.forEach(
            (item) => { this.blocksMap[item.id] = item; },
          );
          newBlocks = this.blocks.concat(newBlocks);
          this.blocks = newBlocks;
          this.status.offset = newBlocks.length;
          this.status.hasNext = !(next === null);
          this.status.loading = false;
        },
        () => { this.status.loading = false; },
      );
    },
  },
  created() {
    bus.bus.on(bus.events.refreshBoards, this.reset);
    this.registerScrollEvent();
    this.initialize();
  },
  beforeUnmount() {
    bus.bus.off(bus.events.refreshBoards, this.reset);
    this.unbindScroll();
  },
};
</script>

<style lang="scss" scoped>
@use 'utils/pin' as *;
@use './utils/fonts' as *;
@use './utils/loader' as *;
@use 'utils/grid-layout' as *;
/* grid */
.grid-item { width: $pin-preview-width; }

/* card */
$pin-footer-position-fix: -6px;
$avatar-width: 30px;
$avatar-height: 30px;
.board-card{
  .preview-image {
    background-color: var(--pinry-image-background);
  }
  .card-image > img {
    min-width: $pin-preview-width;
    background-color: var(--pinry-image-background);
    border-radius: 3px 3px 0 0;
    @include loader('../assets/loader.gif');
  }
}
.board-footer {
  position: relative;
  top: $pin-footer-position-fix;
  background-color: var(--pinry-card-background);
  border-radius: 0 0 3px 3px ;
  box-shadow: var(--pinry-card-shadow);
  font-weight: bold;
  .description {
    @include secondary-font;
    padding-left: 10px;
    padding-bottom: 5px;
    overflow: hidden;
    text-overflow: ellipsis;
  }
  .board-info {
    padding: 10px;
    color: var(--pinry-title-text);
  }
  .num-pins {
    font-size: 0.8rem;
    color: var(--pinry-title-text);
  }
}
@include screen-grid-layout("#boards-container")

</style>
