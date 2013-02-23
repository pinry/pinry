$(window).load(function() {
    window.lightbox = function(pins) {
        var links = pins.find('.lightbox');

        function createBox(imageUrl) {
            var template = Handlebars.compile($('#lightbox-template').html());
            var html = template({image: imageUrl});
            $('body').append(html);

            $('.lightbox-wrapper img').load(function() {
                $('.lightbox-background').css('height', String($(document).height())+'px');
                $(this).css({
                    'max-width': String($(window).width()-200)+'px',
                    'max-height': String($(window).height()-200)+'px',
                    'margin-top': String($(window).scrollTop()+100)+'px'
                });
                var width = $(this).width();
                $('.lightbox-wrapper').css({
                    'margin-left': '-'+String(width/2)+'px'
                });
            });

            return $('.lightbox-background');
        }

        for (var i=0; i < links.length; i++) {
            link = links.eq(i);
            link.off('click');
            link.click(function(e) {
                var box = createBox($(this).attr('href'));
                box.click(function() {
                    box.remove()
                });
                e.preventDefault();
            });
        }
    }
});
