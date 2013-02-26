$(window).load(function() {
    var scrollLevel = 0;

    window.lightbox = function(pins) {
        var links = pins.find('.lightbox');

        function createBox(boxData) {
            var template = Handlebars.compile($('#lightbox-template').html());
            var html = template(boxData);
            $('body').append(html);

            scrollLevel = $(window).scrollTop();
            $('#pins').css({
                'margin-top': String(-scrollLevel)+'px',
                'position': 'fixed'
            });

            $('.lightbox-wrapper img').load(function() {
                $('.lightbox-background').css('height', String($(document).height())+'px');
                $('.lightbox-wrapper').css({
                    'width': boxData.width,
                    'margin-top': String(100)+'px',
                    'margin-left': '-'+String(boxData.width/2)+'px'
                });
            });

            return $('.lightbox-background');
        }

        for (var i=0; i < links.length; i++) {
            link = links.eq(i);
            link.off('click');
            link.click(function(e) {
                var box = createBox({
                    image: $(this).attr('href'),
                    gravatar: $(this).data('gravatar'),
                    username: $(this).data('username'),
                    description: $(this).data('description'),
                    tags: $(this).data('tags').split(','),
                    width: $(this).data('width'),
                    height: $(this).data('height')
                });
                box.click(function() {
                    box.remove()
                    $('#pins').css({
                        'position': 'static',
                        'margin-top': 0
                    });
                    $(window).scrollTop(scrollLevel);
                });
                e.preventDefault();
            });
        }
    }
});
