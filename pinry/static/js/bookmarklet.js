if (!jQuery) {
    var head = document.getElementsByTagName('head')[0];
    var script = document.createElement('script');
    script.src = '//cdnjs.cloudflare.com/ajax/libs/jquery/1.8.3/jquery.min.js';
    head.appendChild(script);
}

$(document).ready(function() { 
    var scriptUri;

    function curScriptUrl(callback) {
        var scripts = document.getElementsByTagName("script");
        var scriptURI = scripts[scripts.length-1].src;  

        if(scriptURI != "") {
            callback(scriptURI);
        } else if($ != undefined) {
            $(document).ajaxSuccess(function(e, xhr, s) {
                callback(s.url);
            }); 
        }
    }

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
            var apiUrl = 'http://';
            curScriptUrl(function(x) {
                scriptUri = x;
                apiUrl = apiUrl +scriptUri.split('/')[2];
            });
            apiUrl = apiUrl + '/pins/pin-form/?pin-image-url='+imageUrl;
            window.open(apiUrl, '1361920530821', 'width=579,height=475,toolbar=0,menubar=0,location=0,status=1,scrollbars=1,resizable=1,left=0,top=0');
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
