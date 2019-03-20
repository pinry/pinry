var events = new Vue({});
var eventsName = {
  pinReflowDone: "single-pin-reflow-done",
  allPinReflowDone: "all-pin-reflow-done",
  pinView: {
    open: "view-single-pin",
    close: "close-pin-view",
  },
};

function fetchPins(offset) {
    var apiUrl = API_BASE + 'pins/?format=json&ordering=-id&limit=50&offset='+String(offset);
    if (tagFilter) apiUrl = apiUrl + '&tags__name=' + tagFilter;
    if (userFilter) apiUrl = apiUrl + '&submitter__username=' + userFilter;
    return axios.get(apiUrl)
}

var utils = {
  getDocumentHeight: function () {
    var body = document.body,
    html = document.documentElement;
    return Math.max(
      body.scrollHeight, body.offsetHeight,
      html.clientHeight, html.scrollHeight,
      html.offsetHeight,
    );
  },
  getWindowHeight: function () {
    return window.innerHeight
  }
};

function EventCounter(countEvent, triggerEvent, triggerTimes) {

  var self = {
    id: new Date().getTime(),
    count: 0,
    targetCount: triggerTimes,
    triggerEvent: countEvent,
    countEvent: countEvent,
  };
  events.$on(
    countEvent,
    function() {
      self.count += 1;
      if (self.count >= self.targetCount) {
        events.$emit(triggerEvent)
      }
    }
  );
  self.resetAfterReflow = function (targetCount) {
    self.count = 0;
    self.targetCount = targetCount;
  };
  self.reset = function (targetCount) {
    self.targetCount = targetCount;
  };

  return self;
}


function HeightTable(blockMargin) {
  var self = {
    data: {}
  };
  function get(obj, index) {
    if (!obj.data.hasOwnProperty(index)) {
      return null
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

  self.get = function(index) {
    return get(self, index);
  };

  self.set = function (index, value) {
    return set(self, index, value)
  };
  self.getHeightOffset = function (index, rowSize) {
    return getHeightOffset(self, index, rowSize);
  };
  self.getMaxHeight = function(rowSize, blockMargin) {
    var size = Object.keys(self.data).length;
    var heightArray = [];
    for (var column = 0; column < rowSize; column ++) {
      heightArray.push(0);
    }
    for (var index = 0; index < size; index++) {
      var column = index % rowSize;
      heightArray[column] = heightArray[column] + self.get(index) + blockMargin;
    }
    return Math.max(...heightArray);
  };
  return self;
}


Vue.component(
  'light-box',
  {
    data: function () {
      return {
        backgroundStyle: null,
        lightBoxWrapperStyle: null,
        lightBoxImageWrapperStyle: null,
      }
    },
    props: ['pin'],
    template: "#lightbox-template",
    mounted: function () {
      var documentHeight = utils.getDocumentHeight();
      var imageWidth = this.pin.image.standard.width;
      var imageHeight = this.pin.image.standard.height;
      var windowHeight = utils.getWindowHeight();
      var backgroundHeight = documentHeight;
      var lightBoxWrapperStyle = {
        'width': imageWidth + "px",
        'marginTop': '80px',
        'marginBottom': '80px',
        'margin-left': - imageWidth / 2 + "px",
      };
      var wrapper = this.$el.querySelector(".lightbox-wrapper");

      if (wrapper.getBoundingClientRect().height + 140 > windowHeight) {
        var wrapperHeight = wrapper.getBoundingClientRect().height;
        backgroundHeight = wrapperHeight + 160;
      }
      this.backgroundStyle = {
        height: backgroundHeight + 'px',
      };
      this.lightBoxImageWrapperStyle = {
        height: imageHeight + 'px',
      };
      this.lightBoxWrapperStyle = lightBoxWrapperStyle;
    },
    methods: {
      onCloseView: function() {
        events.$emit(eventsName.pinView.close);
      }
    }
  }
);


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
  updated: function() {
    events.$emit(eventsName.pinReflowDone);
  },
  methods: {
    showImageDetail: function(event) {
      events.$emit(eventsName.pinView.open, this.pin);
      if (event) event.preventDefault();
    },
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
      "counter": null,
      "containerStyle": null,
      status: {
        loading: true,
        hasNext: true,
        offset: 0,
      },
    };
  },
  template: "#pin-container-template",
  created: function() {
    this.heightTable = HeightTable(this.args.blockMargin);
    this.loadMore();
    var self = this;
    window.addEventListener("optimizedResize", function() {
      self.reflow();
    });
    self.bindScrollHandler();
    self.counter = EventCounter(
      eventsName.pinReflowDone,
      eventsName.allPinReflowDone,
      self.pins.length,
    );
    events.$on(eventsName.allPinReflowDone, this.updateContainerStyle);
  },
  mounted: function() {
    this.reflow();
  },
  methods: {
    updateContainerStyle: function() {
      var height = this.heightTable.getMaxHeight(
        this.args.rowSize,
        this.args.blockMargin,
      );
      this.containerStyle = {
        height: height + "px",
      };
    },
    loadMore() {
      var self = this;
      self.markAsLoading();
      fetchPins(self.status.offset).then(
        function (res) {
          var newPins = self.pins.concat(res.data.results);
          self.counter.reset(newPins.length);
          self.pins = newPins;
          self.status.offset += res.data.results.length;
          if (res.data.next === null) {
            self.markAsLoaded(false);
          } else {
            self.markAsLoaded(true);
          }
        },
      );
    },
    markAsLoaded: function(hasNext) {
      this.status.hasNext = hasNext;
      this.status.loading = false;
      this.$emit(
          "loaded",
      );
      if (!hasNext) {
        this.$emit("no-more-pins")
      }
    },
    markAsLoading: function() {
      this.status.loading = true;
      this.$emit(
          "loading",
      );
    },
    bindScrollHandler: function () {
      var self = this;

      function getDocumentScrollTop() {
        var doc = document.documentElement;
        return (window.pageYOffset || doc.scrollTop)  - (doc.clientTop || 0);
      }

      scrollHandler = function() {
        if (self.status.loading || !self.status.hasNext) {
          return
        }
        var windowPosition = getDocumentScrollTop() + window.innerHeight;
        var bottom = utils.getDocumentHeight() - 100;
        if(windowPosition > bottom) {
          self.loadMore();
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
      this.counter.resetAfterReflow(self.pins.length);
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
      noMore: false,
      currentPin: null,
    }
  },
  created: function() {
    events.$on(
      eventsName.pinView.open,
      this.onViewPin,
    );
    events.$on(
      eventsName.pinView.close,
      this.onClosePin,
    );
  },
  methods: {
    onViewPin: function(pin) {
      this.currentPin = pin;
    },
    onClosePin: function(pin) {
      this.currentPin = null;
    },
    onLoaded: function(){
      this.loading = false;
    },
    onLoading: function(){
      this.loading = true;
    },
    onNoMore: function () {
      this.noMore = true;
    }
  },
});
