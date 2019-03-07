var events = new Vue({});

function fetchPins(offset) {
    var apiUrl = API_BASE + 'pins/?format=json&ordering=-id&limit=50&offset='+String(offset);
    if (tagFilter) apiUrl = apiUrl + '&tags__name=' + tagFilter;
    if (userFilter) apiUrl = apiUrl + '&submitter__username=' + userFilter;
    return axios.get(apiUrl)
}


function HeightTable(blockMargin) {
  var self = {
    data: {}
  };
  function get(obj, index) {
    if (!obj.data.hasOwnProperty(index)) {
      obj.data[index] = null
    }
    return obj.data[index];
  }

  function set(obj, index, value) {
    if (!obj.data.hasOwnProperty(index)) {
      obj.data[index] = value
    }
    return obj.data[index];
  }

  function getHeightOffset(obj, indexOfElement, rowSize) {
    var height = 0;
    for (var index = rowSize - 1; index < indexOfElement; index += rowSize) {
      var value = obj.get(index);
      if (value === null) {
        console.log("Error occurs while loading elements's height offset");
        return null
      }
      height += (value + blockMargin);
    }
    return height
  }

  self.get = function(index, value) {
    return get(self, index, value);
  };

  self.set = function (index, value) {
    return set(self, index, value)
  };
  self.getHeightOffset = function (index, rowSize) {
    return getHeightOffset(self, index, rowSize);
  };
  return self;
}


Vue.component('pin', {
  data: function () {
    return {
      'loaded': false,
      'editable': true,
      'active': false,
      'imageStyle': null,
      'pinStyle': null,
      'height': null,
      'heightOffset': null,
    }
  },
  props: ['pin', 'args', 'index', 'heightTable'],
  template: '#pin-template',
  created: function() {
    var self = this;
    events.$on("reflow", function () {
      self.reflow();
    });
  },
  mounted: function() {
    this.reflow();
    this.$emit("rendered", {index: this.index, height: this.height});
  },
  methods: {
    reflow: function() {
      this.heightOffset = this.heightTable.getHeightOffset(this.index, this.args.rowSize);
      this.imageStyle = this.getImageStyle();
      this.pinStyle = this.getPinStyle();
      this.height = this.getTextHeight() + this.pin.image.thumbnail.height;
    },
    getImageStyle: function() {
      return {
        width: this.pin.image.thumbnail.width + 'px',
        height: this.pin.image.thumbnail.height + 'px',
      }
    },
    getPinStyle: function() {
      var self = this;
      var marginTop = self.heightOffset;
      var marginLeft = 0;

      function isFirstOne(rowSize, index) {
        index = index + 1;
        if ((index % rowSize) === 1 ){
          return true;
        }
      }

      function getRowNumber(rowSize, index) {
        index = index + 1;
        var rowNumber = Math.floor(index % rowSize);
        if (rowNumber === 0) {
          return rowSize;
        }
        return rowNumber;
      }

      if (isFirstOne(self.args.rowSize, self.index)) {
        marginLeft = self.args.rowStartMargin;
      } else {
        var marginPerBlock = self.args.blockWidth + self.args.blockMargin;
        var rowNumber = getRowNumber(self.args.rowSize, self.index);
        marginLeft = self.args.rowStartMargin + marginPerBlock * (rowNumber - 1);
      }
      return {
        'margin-left': marginLeft + 'px',
        'margin-top': marginTop + 'px',
      };
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
      var element = this.$el.querySelector(".pin-description");
      return element.getBoundingClientRect().height;
    },
  }
});


Vue.component('pin-container', {
  data: function () {
    return {
      args: {
        "containerWidth": 0,
        "blockWidth": 240,
        "blockMargin": 15,
        "rowSize": 0,
        "rowStartMargin": 0,
        "rowEndMargin": 0,
      },
      "pins": [],
      "heightTable": [],
      "counter": 0,
      "loading": true,
    };
  },
  template: "#pin-container-template",
  created: function() {
    this.heightTable = HeightTable(this.args.blockMargin);
    this.markAsLoading();
    var self = this;
    var offset = 0;
    fetchPins(offset).then(
      function (res) {
        self.pins = res.data.results;
        self.markAsLoaded();
      },
    );
    window.addEventListener("optimizedResize", function() {
      self.reflow();
    });
  },
  mounted: function() {
    this.reflow();
  },
  methods: {
    markAsLoaded: function() {
      this.loading = false;
      this.$emit(
          "loaded",
      );
    },
    markAsLoading: function() {
      this.loading = true;
      this.$emit(
          "loading",
      );
    },
    scrollHandler: function () {
      var self = this;

      function getDocumentScrollTop() {
        var doc = document.documentElement;
        return (window.pageYOffset || doc.scrollTop)  - (doc.clientTop || 0);
      }

      function getDocumentHeight() {
        var body = document.body,
        html = document.documentElement;
        return Math.max(
          body.scrollHeight, body.offsetHeight,
          html.clientHeight, html.scrollHeight,
          html.offsetHeight,
        );
      }
      scrollHandler = function() {
        if (self.loading) {
          return
        }
        console.log('loading...');
        var windowPosition = getDocumentScrollTop() + window.innerHeight;
        var bottom = getDocumentHeight() - 100;
        if(windowPosition > bottom) {
          self.loadMore()
        }
      };
      window.addEventListener('scroll', function(e) {
          scrollHandler();
        }
      );
    },
    updateChildHeight: function(childArg) {
      this.heightTable.set(childArg.index, childArg.height);
    },
    reflow: function() {
      this.updateArguments();
      events.$emit("reflow");
    },
    updateArguments: function() {
      var blockContainer = this.$el;
      var containerWidth = blockContainer.clientWidth;
      var blockMargin = this.args.blockMargin,
          blockWidth = this.args.blockWidth,
          rowSize = Math.floor(containerWidth / (blockWidth + blockMargin));
      var rowStartMargin = (containerWidth - rowSize * (blockWidth + blockMargin)) / 2 ;
      var rowEndMargin = rowStartMargin - blockMargin;

      this.args.containerWidth = containerWidth;
      this.args.blockWidth = blockWidth;
      this.args.blockMargin = blockMargin;
      this.args.rowSize = rowSize;
      this.args.rowStartMargin = rowStartMargin;
      this.args.rowEndMargin = rowEndMargin;
    },
  },
});

(function() {
  var previousResize = 0;
  var throttle = function(type, name, obj) {
      obj = obj || window;
      var running = false;
      var func = function() {
          if (running) { return; }
          var now = new Date().getTime();
          if ((now - previousResize) < 200) {
            return
          }
          previousResize = now;
          running = true;
           requestAnimationFrame(function() {
              obj.dispatchEvent(new CustomEvent(name));
              running = false;
          });
      };
      obj.addEventListener(type, func);
  };

  throttle("resize", "optimizedResize");
})();


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
