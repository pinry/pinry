<template>
  <div class="pins">
    <section class="section">
      <div id="pins-container" class="container" v-if="blocks">
        <div
          v-masonry=""
          transition-duration="0.3s"
          item-selector=".grid-item"
          column-width=".grid-sizer"
          gutter=".gutter-sizer"
        >
          <template v-for="item in blocks">
            <div v-bind:key="item.id"
                 v-masonry-tile
                 :class="item.class"
                 class="grid pin-masonry">
              <div class="grid-sizer"></div>
              <div class="gutter-sizer"></div>
              <div class="pin-card grid-item">
                <img :src="item.url"
                     @load="onPinImageLoaded(item.id)"
                     @click="openPreview(item)"
                     alt="item.description"
                     :style="item.style"
                     class="pin-preview-image">
                <div class="pin-footer">
                  <div class="description" v-show="item.description"><p>{{ item.description }}</p>
                  </div>
                  <div class="details">
                    <div class="is-pulled-left">
                      <img class="avatar" :src="item.avatar" alt="">
                    </div>
                    <div class="pin-info">
                      <span class="dim">pined by&nbsp;
                        <span>
                          <router-link
                            :to="{ name: 'user', params: {user: item.author} }">
                            {{ item.author }}
                          </router-link>
                        </span>
                        <template v-if="item.tags.length > 0">
                          &nbsp;in&nbsp;
                          <template v-for="tag in item.tags">
                            <span v-bind:key="tag" class="pin-tag">
                              <router-link :to="{ name: 'tag', params: {tag: tag} }"
                                           params="{tag: tag}">{{ tag }}</router-link>
                            </span>
                          </template>
                        </template>
                      </span>
                    </div>
                    <div class="is-clearfix"></div>
                  </div>
                </div>
              </div>
            </div>
          </template>
        </div>
      </div>
      <loadingSpinner v-bind:show="status.loading"></loadingSpinner>
      <noMore v-bind:show="!status.hasNext"></noMore>
    </section>
  </div>
</template>

<script>
import API from './api';
import pinHandler from './utils/PinHandler';
import PinPreview from './PinPreview.vue';
import loadingSpinner from './loadingSpinner.vue';
import noMore from './noMore.vue';
import scroll from './utils/scroll';

function createImageItem(pin) {
  const image = {};
  image.url = pinHandler.escapeUrl(pin.image.thumbnail.image);
  image.id = pin.id;
  image.description = pin.description;
  image.tags = pin.tags;
  image.author = pin.submitter.username;
  image.avatar = `//gravatar.com/avatar/${pin.submitter.gravatar}`;
  image.large_image_url = pinHandler.escapeUrl(pin.image.image);
  image.original_image_url = pin.url;
  image.referer = pin.referer;
  image.orgianl_width = pin.image.width;
  image.style = {
    width: `${pin.image.thumbnail.width}px`,
    height: `${pin.image.thumbnail.height}px`,
  };
  image.class = {};
  return image;
}

export default {
  name: 'pins',
  components: {
    loadingSpinner,
    noMore,
  },
  data() {
    return {
      blocks: [],
      blocksMap: {},
      status: {
        loading: false,
        hasNext: true,
        offset: 0,
      },
    };
  },
  props: {
    pinFilters: {
      type: Object,
      default() {
        return {
          tagFilter: null,
          userFilter: null,
        };
      },
    },
  },
  methods: {
    onPinImageLoaded(itemId) {
      this.blocksMap[itemId].class = {
        'image-loaded': true,
      };
    },
    registerScrollEvent() {
      const self = this;
      scroll.bindScroll2Bottom(
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
          const item = createImageItem(pin);
          blocks.push(
            item,
          );
        },
      );
      return blocks;
    },
    openPreview(pinItem) {
      this.$buefy.modal.open(
        {
          parent: this,
          component: PinPreview,
          props: {
            pinItem,
          },
          scroll: 'keep',
          customClass: 'pin-preview-at-home',
        },
      );
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
      this.status.loading = true;
      let promise;
      if (this.pinFilters.tagFilter) {
        promise = API.fetchPins(this.status.offset, this.pinFilters.tagFilter);
      } else if (this.pinFilters.userFilter) {
        promise = API.fetchPins(this.status.offset, null, this.pinFilters.userFilter);
      } else if (this.pinFilters.boardFilter) {
        promise = API.fetchPinsForBoard(this.pinFilters.boardFilter);
      } else {
        promise = API.fetchPins(this.status.offset);
      }
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
    this.registerScrollEvent();
    this.fetchMore(true);
  },
};
</script>

<style lang="scss" scoped>
/* grid */
.grid-sizer,
.grid-item { width: 240px; }
.grid-item {
  margin-bottom: 15px;
}
.gutter-sizer {
  width: 15px;
}

/* pin-image transition */
.pin-masonry.image-loaded{
  opacity: 1;
  transition: opacity .3s;
}
.pin-masonry {
  opacity: 0;
}

/* card */
$pin-footer-position-fix: -6px;
$avatar-width: 30px;
$avatar-height: 30px;

@mixin pin-detail-font-size{
  font-size: 12px;
}

@mixin description-font {
  @include pin-detail-font-size;
  font-family: 'Georgia', 'Times', 'Times New Roman', serif;
}

@mixin secondary-font {
  @include pin-detail-font-size;
  color: #999;
  font-weight: normal;
}

@mixin loader {
  background: url('../assets/loader.gif');
  background-position: center center;
  background-repeat: no-repeat;
}

.pin-card{
  .pin-preview-image {
    cursor: zoom-in;
  }
  > img {
    background-color: white;
    border-radius: 3px 3px 0 0;
    @include loader;
  }
  .avatar {
    height: $avatar-height;
    width: $avatar-width;
    border-radius: 3px;
  }
  .pin-tag {
    margin-right: 0.2rem;
  }
}
.pin-footer {
  position: relative;
  top: $pin-footer-position-fix;
  background-color: white;
  border-radius: 0 0 3px 3px ;
  box-shadow: 0 1px 0 #bbb;
  .description {
    @include description-font;
    padding: 8px;
    border-bottom: 1px solid #DDDDDD;
    overflow: hidden;
    text-overflow: ellipsis;
  }
  .details {
    @include secondary-font;
    padding: 10px;
    > .pin-info {
      line-height: 16px;
      width: 220px;
      padding-left: $avatar-width + 5px;
    }
    .pin-info a {
      font-weight: bold;
    }
  }
}

/*pin container size fit*/
/* Generated by python code:
/* def fn(x):
/*     gutter = 15
/*     image_width = 240
/*     border_width_of_parent = 24
/*     size = image_width * x + gutter * (x - 1)
/*     width = size + border_width_of_parent * 2
/*     print(template % (width, size))
/*
/* for i in range(1, 12):
/*     fn(i)
*/

@media screen and (min-width: 288px) {
  #pins-container {
    max-width: 240px;
  }
}
@media screen and (min-width: 543px) {
  #pins-container {
    max-width: 495px;
  }
}
@media screen and (min-width: 798px) {
  #pins-container {
    max-width: 750px;
  }
}
@media screen and (min-width: 1053px) {
  #pins-container {
    max-width: 1005px;
  }
}
@media screen and (min-width: 1308px) {
  #pins-container {
    max-width: 1260px;
  }
}
@media screen and (min-width: 1563px) {
  #pins-container {
    max-width: 1515px;
  }
}
@media screen and (min-width: 1818px) {
  #pins-container {
    max-width: 1770px;
  }
}
@media screen and (min-width: 2073px) {
  #pins-container {
    max-width: 2025px;
  }
}
@media screen and (min-width: 2328px) {
  #pins-container {
    max-width: 2280px;
  }
}
@media screen and (min-width: 2583px) {
  #pins-container {
    max-width: 2535px;
  }
}
@media screen and (min-width: 2838px) {
  #pins-container {
    max-width: 2790px;
  }
}
</style>
