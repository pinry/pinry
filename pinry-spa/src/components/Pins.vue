<template>
  <div class="pins">
    <section class="section">
      <div class="container">
        <bricks
          ref="bricks"
          :data="waterfallData"
          :sizes="waterfallSizes"
          :offset="100"
          @reach="fetchWaterfallData(true)"
          @update="done"
          @pack="done"
        >
          <template slot-scope="scope">
           <div class="card">
              <img v-if="scope.item.src" class="card-img-top" :src="scope.item.src" :alt="scope.item.index">
              <div class="card-block">
                <h4 class="card-title" :style="scope.item.style">{{ scope.item.index }}</h4>
                <p class="card-text">{{ scope.item.width }} * {{ scope.item.height }}</p>
              </div>
            </div>
          </template>
        </bricks>
        <div class="loading" :class="{ active: loading }">
          <div>Loading</div>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
import Bricks from 'vue-bricks';
import API from './api';

export default {
  name: 'pins',
  components: {
    Bricks,
  },
  data() {
    return {
      loading: true,
      waterfallData: [],
      waterfallSizes: [
        { columns: 4, gutter: 20 },
        { mq: '414px', columns: 1, gutter: 10 },
        { mq: '640px', columns: 1, gutter: 80 },
        { mq: '800px', columns: 2, gutter: 80 },
        { mq: '1024px', columns: 3, gutter: 15 },
        { mq: '1280px', columns: 3, gutter: 30 },
        { mq: '1366px', columns: 4, gutter: 15 },
        { mq: '1440px', columns: 4, gutter: 30 },
        { mq: '1980px', columns: 5, gutter: 40 },
      ],
    };
  },
  methods: {
    done() {
      this.loading = false;
    },
    fetchWaterfallData() {
      return new Promise((resolve) => {
        this.loading = true;
        API.fetchPins(0).then(
          (resp) => {
            const data = resp.data.results;
            const count = data.length;
            const items = [];
            let i = 0;
            let image;
            let lastIndex = 0;
            for (image in data) {
              if (!data.hasOwnProperty(image)) {
                  
              }else{
                items[i] = {
                  index: lastIndex,
                  style: {},
                  width: data.image.thumbnail.width,
                  height: data.image.thumbnail.height,
                };
                lastIndex += 1;
              }
            }
            this.waterfallData = data;
            resolve(data);
          },
        );
      });
    },
  },
  created() {
    this.fetchWaterfallData();
  },
};
</script>

<style scoped>

</style>
