
function fetchPins(offset) {
    var apiUrl = API_BASE + 'pins/?format=json&ordering=-id&limit=50&offset='+String(offset);
    if (tagFilter) apiUrl = apiUrl + '&tags__name=' + tagFilter;
    if (userFilter) apiUrl = apiUrl + '&submitter__username=' + userFilter;
    return axios.get(apiUrl)
}


function HeightTable(rowSize) {
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

  function getHeightOffset(obj, indexOfElement) {
    if (indexOfElement <= rowSize) {
      return 0;
    }
    var height = 0;
    for (var index = 0; index < indexOfElement; index += rowSize) {
      var value = obj.get(index);
      if (value === null) {
        return null
      }
      height += value;
    }
    return height
  }

  self.get = function(index, value) {
    return get(self, index, value);
  };

  self.set = function (index, value) {
    return set(self, index, value)
  };
  self.getHeightOffset = function (index) {
    return getHeightOffset(self, index);
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
  mounted: function() {
    this.heightOffset = this.heightTable.getHeightOffset(this.index);
    this.imageStyle = this.getImageStyle();
    this.pinStyle = this.getPinStyle();
    this.height = this.getTextHeight() + this.pin.image.thumbnail.height;
    this.$emit("rendered", {index: this.index, height: this.height});
  },
  methods: {
    getImageStyle: function() {
      return {
        width: this.pin.image.thumbnail.width + 'px',
        height: this.pin.image.thumbnail.height + 'px',
      }
    },
    getPinStyle: function() {
      var self = this;

      var marginLeft = 0;
      var marginTop = 0;

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
          return 7;
        }
        return rowNumber;
      }

      function getLineNumber(rowSize, index) {
        return Math.floor((index) / rowSize);
      }

      if (self.index < self.args.rowSize) {
        marginTop = 0;
      } else {
        var lineNumber = getLineNumber(self.args.rowSize, self.index);
        marginTop = (self.args.blockMargin + self.heightOffset) * lineNumber;
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
      var height = element.getBoundingClientRect().height;
      return height
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
    };
  },
  template: "#pin-container-template",
  created: function() {
    this.heightTable = HeightTable(this.rowSize);
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
    window.addEventListener("resize", this.reflow, {})
  },
  mounted: function() {
    this.reflow();
  },
  methods: {
    updateChildHeight: function(childArg) {
      this.heightTable.set(childArg.index, childArg.height);
    },
    reflow: function() {
      this.updateArguments();
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
