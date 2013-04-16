/**
 * Pinry
 * Descrip: Core of pinry, loads and tiles pins.
 * Authors: Pinry Contributors
 * Updated: Apr 5th, 2013
 * Require: jQuery, Pinry JavaScript Helpers
 */


$(window).load(function() {
    /**
     * tileLayout will simply tile/retile the block/pin container when run. This
     * was put into a function in order to adjust frequently on screen size 
     * changes.
     */
    window.tileLayout = function() {
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
                'margin-top':  colHeights[sCol],
            });
            block.fadeIn(300);
            colHeights[sCol] += block.height()+(blockMargin);
        }

        // Edit pin if pencil icon clicked
        $('.icon-pencil').each(function() {
            var thisPin = $(this);
            $(this).off('click');
            $(this).click(function() {
                $(this).off('click');
                pinForm($(this).data('id'));
            });
        });

        // Delete pin if trash icon clicked
        $('.icon-trash').each(function() {
            var thisPin = $(this);
            $(this).off('click');
            $(this).click(function() {
                $(this).off('click');
                var promise = deletePinData($(this).data('id'));
                promise.success(function() {
                    thisPin.closest('.pin').remove();
                    tileLayout();
                });
                promise.error(function() {
                    message('Problem deleting image.', 'alert alert-error');
                });
            });
        });

        // Show edit-buttons only on mouse over
        $('.pin').each(function(){
            var thisPin = $(this);
            thisPin.find('.editable').hide();
            thisPin.off('hover');
            thisPin.hover(function() {
                thisPin.find('.editable').stop(true, true).fadeIn(300);
            }, function() {
                thisPin.find('.editable').stop(true, false).fadeOut(300);
            });
        });

        $('.spinner').css('display', 'none');
        blockContainer.css('height', colHeights.sort().slice(-1)[0]);
    }

    /**
     * On scroll load more pins from the server
     */
    window.scrollHandler = function() {
        var windowPosition = $(window).scrollTop() + $(window).height();
        var bottom = $(document).height() - 100;
        if(windowPosition > bottom) loadPins();
    }

    /**
     * Load our pins using the pins template into our UI, be sure to define a
     * offset outside the function to keep a running tally of your location.
     */
    function loadPins() {
        // Disable scroll
        $(window).off('scroll');

        // Show our loading symbol
        $('.spinner').css('display', 'block');

        // Fetch our pins from the api using our current offset
        var apiUrl = '/api/v1/pin/?format=json&order_by=-id&offset='+String(offset);
        if (tagFilter) apiUrl = apiUrl + '&tag=' + tagFilter;
        if (userFilter) apiUrl = apiUrl + '&submitter__username=' + userFilter;
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
            tileLayout();
            lightbox();
            $('#pins').ajaxStop(function() {
                $('img').load(function() {
                    $(this).fadeIn(300);
                });
            });

            if (pins.objects.length < apiLimitPerPage) {
                $('.spinner').css('display', 'none');
                if ($('#pins').length != 0) {
                    var theEnd = document.createElement('div');
                    theEnd.id = 'the-end';
                    $(theEnd).html('&mdash; End &mdash;');
                    $(theEnd).css('padding', 50);
                    $('body').append(theEnd);
                }
            } else {
                $(window).scroll(scrollHandler);
            }
        });

        // Up our offset, it's currently defined as 50 in our settings
        offset += apiLimitPerPage;
    }


    // Set offset for loadPins and do our initial load
    var offset = 0;
    loadPins();

    // If our window gets resized keep the tiles looking clean and in our window
    $(window).resize(function() {
        tileLayout();
        lightbox();
    })
});
