$(window).load(function() {
    /**
     * tileLayout will simply tile/retile the block/pin container when run. This
     * was put into a function in order to adjust frequently on screen size 
     * changes.
     */
    function tileLayout() {
        var blockContainer = $('#pins'),
            blocks = blockContainer.children('.pin'),
            blockMargin = 15,
            blockWidth = 240,
            rowSize = Math.floor(blockContainer.width()/(blockWidth+blockMargin)),
            colHeights = [],
            rowMargins = [],
            marginLeft = 0;

        // Fill our colHeights array with 0 for each row we have
        for (var i=0; i < rowSize; i++) colHeights[i] = 0;

        // Fill out our rowMargins which will be static after this
        for (var i=0; i < rowSize; i++) {
            // Our first item has a special margin to keep things centered
            if (i == 0) rowMargins[0] = (blockContainer.width()-rowSize*(blockWidth+blockMargin))/2;
            else rowMargins[i] = rowMargins[i-1]+(blockWidth+blockMargin);
        }

        // Loop through every block
        for (var b=0; b < blocks.length; b++) {
            // Get the jQuery object of the current block
            block = blocks.eq(b);

            // Position our new pin in the shortest column
            var sCol = 0;
            for (var i=0; i < rowSize; i++) {
                if (colHeights[sCol] > colHeights[i]) sCol = i;
            }

            block.css({
                'margin-left': rowMargins[sCol],
                'margin-top': colHeights[sCol],
                'display': 'block'
            });

            colHeights[sCol] += block.height()+(blockMargin);
        }

        lightbox(blocks);
        $('.spinner').css('display', 'none');
        blockContainer.css('height', colHeights.sort().slice(-1)[0]);
    }


    /**
     * Load our pins using the pins template into our UI, be sure to define a
     * offset outside the function to keep a running tally of your location.
     */
    function loadPins() {
        // Show our loading symbol
        $('.spinner').css('display', 'block');

        // Fetch our pins from the api using our current offset
        var apiUrl = '/api/v1/pin/?format=json&order_by=-id&offset='+String(offset);
        if (tagFilter) apiUrl = apiUrl + '&tag=' + tagFilter;
        $.get(apiUrl, function(pins) {
            // Set which items are editable by the current user
            for (var i=0; i < pins.objects.length; i++) 
                pins.objects[i].editable = (pins.objects[i].submitter.username == currentUser.username);

            // Use the fetched pins as our context for our pins template
            var template = Handlebars.compile($('#pins-template').html());
            var html = template({pins: pins.objects});

            // Append the newly compiled data to our container
            $('#pins').append(html);

            // We need to then wait for images to load in and then tile
            $('#pins').ajaxStop(function() {
                $('img').load(function() {
                    tileLayout();
                });
            });

            // Up our offset, it's currently defined as 30 in our settings
            offset += apiLimitPerPage;
        });
    }


    // Set offset for loadPins and do our initial load
    var offset = 0;
    loadPins();

    // If our window gets resized keep the tiles looking clean and in our window
    $(window).resize(function() {
        tileLayout();
    })

    // If we scroll to the bottom of the document load more pins
    $(window).scroll(function() {
         if($(window).scrollTop() + $(window).height() > $(document).height() - 100) {
            loadPins();
         }
     });
});
