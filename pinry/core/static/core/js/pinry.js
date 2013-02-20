$(window).load(function() {
    function tileLayout() {
        // Config
        var blockMargin = 20;
        var blockWidth = 240;
        // End Config

        var blockContainer = $('#pins');
        var blocks = blockContainer.children('.pin');
        var rowSize = Math.floor(blockContainer.width()/blockWidth);
        var blockWidth = (blockContainer.width()-blockMargin*(rowSize))/rowSize;
        var colHeights = []

        for (var i=0; i < rowSize; i++) {
            colHeights[i] = 0;
        }

        for (var b=0; b < blocks.length; b++) {
            block = blocks.eq(b);

            var col = -1;
            var colHeight = 0;
            for (var i=0; i < rowSize; i++) {
                if (col < 0) {
                    col = 0;
                    colHeight = colHeights[col];
                } else {
                    if (colHeight > colHeights[i]) {
                        col = i;
                        colHeight = colHeights[col];
                    }
                }
            }

            block.css({
                'margin-left': blockWidth*col+col*blockMargin
            });

            blockMarginTop = blockMargin;
            block.css({
                'margin-top': colHeight+blockMarginTop
            });
            colHeights[col] += block.height()+blockMarginTop;

            block.css('display', 'block');
        }

        $('.spinner').css('display', 'none');
        blockContainer.css('height', colHeights.sort().slice(-1)[0]);
    }

    var offset = 0;

    function loadPins() {
        $('.spinner').css('display', 'block');
        $.get('/api/v1/pin/?format=json&offset='+String(offset), function(pins) {
            console.log(pins.objects[0])
            var source = $('#pins-template').html();
            var template = Handlebars.compile(source);
            var context = {
                pins: pins.objects
            }
            var html = template(context);
            $('#pins').append(html);

            $('#pins').ajaxStop(function() {
                tileLayout();
            });

            offset += 30;
        });
    }

    loadPins();

    $(window).resize(function() {
        tileLayout();
    })

    $(window).scroll(function() {
         if($(window).scrollTop() + $(window).height() > $(document).height() - 100) {
            loadPins();
         }
     });
});
