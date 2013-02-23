$(window).load(function() {
    window.lightbox = function(pins) {
        var links = pins.find('.lightbox');

        function createBox(boxData) {
            var template = Handlebars.compile($('#lightbox-template').html());
            var html = template(boxData);
            $('body').append(html);

            $('.lightbox-wrapper img').load(function() {
                $('.lightbox-background').css('height', String($(document).height())+'px');
                $(this).css({
                    'max-width': String($(window).width()-200)+'px',
                    'max-height': String($(window).height()-300)+'px',
                });
                var width = $(this).width();
                $('.lightbox-wrapper').css({
                    'margin-top': String($(window).scrollTop()+100)+'px',
                    'margin-left': '-'+String(width/2)+'px'
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
                    tags: $(this).data('tags').split(',')
                });
                box.click(function() {
                    box.remove()
                });
                e.preventDefault();
            });
        }
    }
});
