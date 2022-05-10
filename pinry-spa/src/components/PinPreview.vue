<template>
  <div class="pin-preview-modal">
    <section>
        <div class="card">
          <div class="card-image">
            <figure class="image">
              <img :src="pinItem.large_image_url" alt="Image">
            </figure>
          </div>
          <div class="card-content">
            <div class="content">
                <p class="description title" v-html="niceLinks(pinItem.description)"></p>
            </div>
            <div class="media">
              <div class="media-left">
                <figure class="image is-48x48">
                  <img :src="pinItem.avatar" alt="Image">
                </figure>
              </div>
              <div class="media-content">
                <div class="is-pulled-left">
                  <p class="title is-4 pin-meta-info"><span class="dim">{{ $t("pinnedByTitle") }}</span><span class="author">{{ pinItem.author }}</span></p>
                  <p class="subtitle is-6" v-show="pinItem.tags.length > 0">
                    <span class="subtitle dim">in&nbsp;</span>
                    <template v-for="tag in pinItem.tags">
                      <b-tag v-bind:key="tag" type="is-info" class="pin-preview-tag">{{ tag }}</b-tag>
                    </template>
                  </p>
                </div>
                <div class="is-pulled-right">
                  <a :href="pinItem.referer" target="_blank">
                    <b-button
                        v-show="pinItem.referer !== null"
                        class="meta-link"
                        type="is-warning">
                      {{ $t("sourceButton") }}
                    </b-button>
                  </a>
                  <a :href="pinItem.original_image_url" target="_blank">
                    <b-button
                        v-show="pinItem.original_image_url !== null"
                        class="meta-link"
                        type="is-link">
                        {{ $t("originalImageButton") }}
                    </b-button>
                  </a>
                  <b-button
                      @click="closeAndGoTo"
                      class="meta-link"
                      type="is-success">
                      {{ $t("permalinkButton") }}
                  </b-button>
                </div>
              </div>
            </div>
          </div>
        </div>
    </section>
  </div>
</template>

<script>
import niceLinks from './utils/niceLinks';

export default {
  name: 'PinPreview',
  props: ['pinItem'],
  methods: {
    closeAndGoTo() {
      this.$parent.close();
      this.$router.push(
        { name: 'pin', params: { pinId: this.pinItem.id } },
      );
    },
    niceLinks,
  },
};
</script>

<style lang="scss" scoped>
@import './utils/fonts.scss';

.meta-link {
  margin-left: 0.3rem;
}
.dim {
  @include secondary-font-color-in-dark;
}
.pin-meta-info {
  line-height: 16px;
}
.card {
  background-color: rgba(0, 0, 0, 0.6);
  .content {
    border-bottom: 1px solid #333;
  }
  .card-content {
    .author {
      @include title-font-color-in-dark;
    }
    padding: 0;
    .content {
      padding: 0.3rem;
      margin-bottom: 0;
    }
    .media {
      padding: 0.3rem;
    }
  }
  .description {
    @include title-font;
    @include title-font-color-in-dark;
    font-size: 16px;
    padding: 8px;
  }
}
.pin-preview-tag {
  margin-right: 0.2rem;
  margin-bottom: 2px;
}
/* preview size should always less then screen */
.card-image img {
  padding: 10px;
  margin-left: auto;
  margin-right: auto;
  width: auto;
}
</style>
