
function fetchPins(offset) {
  var apiUrl = API_BASE + 'pins/?format=json&ordering=-id&limit=50&offset='+String(offset);
  if (tagFilter) apiUrl = apiUrl + '&tags__name=' + tagFilter;
  if (userFilter) apiUrl = apiUrl + '&submitter__username=' + userFilter;
  return axios.get(apiUrl)
}

Vue.component('pin', {
  data: function () {
    return {
      'loaded': false,
      'editable': true,
      'active': false,
      'textId': null,
    }
  },
  props: ['pin'],
  template: '#pin-template',
  methods: {
    onImageLoad: function () {
      this.loaded = true;
      this.$emit("resize", this.getTextHeight());
    },
    getAvatar: function () {
      return "//gravatar.com/avatar/" + this.pin.submitter.gravatar;
    },
    getUserLink: function () {
      return "/pins/users/" + this.pin.submitter.username + "/"
    },
    getTagLink: function (tag) {
      return "/pins/tags/" + tag + "/"
    },
    getTextHeight: function() {
      var element = this.$el;
      var height = element.getBoundingClientRect().height;
      return height
    },
  }
});


var app = new Vue({
  el: '#app',
  components: {
    'waterfall': Waterfall.waterfall,
    'waterfall-slot': Waterfall.waterfallSlot,
  },
  data() {
    return {
      pins: [],
      loading: true,
    }
  },
  methods: {
    getInitialPins: function () {
      var self = this;
      var offset = 0;
      fetchPins(offset).then(
        function (res) {
          self.pins = res.data.results;
          self.loading = false;
        }
      );
    },
  },
  created: function () {
    this.getInitialPins();
  },
});
