if (!jQuery) {
    var head = document.getElementsByTagName('head')[0];
    var script = document.createElement('script');
    script.src = '//cdnjs.cloudflare.com/ajax/libs/jquery/1.8.3/jquery.min.js';
    head.appendChild(script);
}

$(document).ready(function() { 
    function createPage() {
        var documentHeight = $(document).height();

        $('body').append('<div class="pinry-images"></div>');
        $('.pinry-images').css({
            'position': 'absolute',
            'z-index': '9001',
            'background': 'rgba(255, 255, 255, 0.7)',
            'top': '0',
            'left': '0',
            'right': '0',
            'height': documentHeight
        });
    }

    function template(imageUrl) {
        var wrapper = document.createElement('div');
        wrapper.class = 'pinry-image-wrapper';
        image = document.createElement('img');
        image.src = imageUrl;
        image = $(image).css({
            'max-width': '200px',
        });
        wrapper = $(wrapper);
        wrapper.append(image);
        wrapper.css({
            'display': 'inline-block',
            'padding': '15px',
            'cursor': 'pointer'
        });
        wrapper.click(function() {
            $.ajax({
                type: "post",
                url: "http://nebula.bythewood.me/api/v1/pin/",
                contentType: 'application/json',
                data: JSON.stringify({
                    url: imageUrl
                })
            });
            $('.pinry-images').remove();
        });
        return wrapper;
    }

    createPage();

    var images = $('body').find('img');
    for (var i=0; i < images.length; i++) {
        var image = images.eq(i);
        var imageHtml = template(image.attr('src'));
        $('.pinry-images').append(imageHtml);
    }
});
