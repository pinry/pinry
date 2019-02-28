
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
      'imageStyle': null,
    }
  },
  props: ['pin'],
  template: '#pin-template',
  mounted: function() {
    this.imageStyle = {
      width: this.pin.image.thumbnail.width + 'px',
      height: this.pin.image.thumbnail.height + 'px',
    };
  },
  methods: {
    getInlineStyle: function() {
      return {};
    },
    onImageLoad: function () {
      this.loaded = true;
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


Vue.component('pin-container', {
  data: function () {
    return {
        "windowWidth": null,
        "blockWidth": "240px",
        "blockMargin": "15px",
        "pins": [],
    };
  },
  template: "#pin-container-template",
  created: function() {
      this.$emit("loading");
      var self = this;
      var offset = 0;
      fetchPins(offset).then(
        function (res) {
          self.pins = res.data.results;
          self.$emit(
            "loaded",
          );
        },
      );
  },
});


var app = new Vue({
  el: '#app',
  data() {
    return {
      loading: true,
    }
  },
  methods: {
    onLoaded: function(){
      this.loading = false;
    },
    onLoading: function(){
      this.loading = true;
    },
  },
});
