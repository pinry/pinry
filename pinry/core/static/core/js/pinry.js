$(window).bind('load', function() {
    $('.pin').wookmark({
        offset: 3,
        itemWidth: 242,
        autoResize: true
    });

    $('.fancybox').fancybox({
        openEffect: 'none',
        closeEffect: 'none'
    });
});
