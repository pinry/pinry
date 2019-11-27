<template>
  <div class="pin-preview-modal">
    <section>
        <div class="card">
          <div class="card-image">
            <figure class="image">
              <img :src="pinItem.original_url" alt="Image">
            </figure>
          </div>
          <div class="card-content">
            <div class="content">
                <p class="description subtitle">{{ pinItem.description }}</p>
            </div>
            <div class="media">
              <div class="media-left">
                <figure class="image is-48x48">
                  <img :src="pinItem.avatar" alt="Image">
                </figure>
              </div>
              <div class="media-content">
                <p class="title is-4">{{ pinItem.author }}</p>
                <p class="subtitle is-6">
                  <span class="subtitle-font">in</span>
                  <template v-for="tag in pinItem.tags">
                    <b-tag v-bind:key="tag" type="is-info" class="pin-preview-tag">{{ tag }}</b-tag>
                  </template>
                </p>
              </div>
            </div>
          </div>
        </div>
    </section>
  </div>
</template>

<script>
export default {
  name: 'PinPreview',
  props: ['pinItem'],
};
</script>

<style lang="scss" scoped>
@import './utils/fonts.scss';

.card {
  background-color: #0C110D;
  .content {
    border-bottom: 1px solid #333;
  }
  .card-content {
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
  width: 100%;
}
</style>
