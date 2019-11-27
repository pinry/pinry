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
            <div class="media">
              <div class="media-left">
                <figure class="image is-48x48">
                  <img :src="pinItem.avatar" alt="Image">
                </figure>
              </div>
              <div class="media-content">
                <p class="title is-4">{{ pinItem.author }}</p>
                <p class="subtitle is-6">
                  <template v-for="tag in pinItem.tags">
                    <b-tag v-bind:key="tag" type="is-info" class="pin-preview-tag">{{ tag }}</b-tag>
                  </template>
                </p>
              </div>
            </div>
            <div class="content">
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
.pin-preview-tag {
  margin-right: 0.2rem;
}
/* preview size should always less then screen */
.image > img {
  max-height: calc(100vh - 225px);
}
</style>
