/**
 * Bookmarklet for Pinry
 * Descrip: This is trying to be as standalone a script as possible hence
 *          why it has built in helpers and such when the rest of the
 *          scripts make use of helpers.js. In the future i want to remove
 *          all dependencies on jQuery.
 * Authors: Pinry Contributors
 * Updated: Mar 4th, 2013
 * Require: None (dynamically loads jQuery if needed)
 */

(function main() {
    'use strict';

    function closePinry() {
        var el = document.getElementById('pinry-images');
        el.parentNode.removeChild(el);
        el = document.getElementById('pinry-bookmarklet');
        el.parentNode.removeChild(el);
    }

    // Start Helper Functions
    function getFormUrl() {
        var src = document.getElementById('pinry-bookmarklet').src;
        src = src.substr(0, src.indexOf('/static/js'));
        return src + '/pins/pin-form/?pin-image-url=';
    }
    // End Helper Functions


    // Start View Functions
    function pageView() {
        var pinryImages = document.createElement('div');
        pinryImages.id = 'pinry-images';
        pinryImages.style.position = 'fixed';
        pinryImages.style.zIndex = 9001;
        pinryImages.style.background = 'rgba(0, 0, 0, 0.7)';
        pinryImages.style.paddingTop = '70px';
        pinryImages.style.top = 0;
        pinryImages.style.bottom = 0;
        pinryImages.style.left = 0;
        pinryImages.style.right = 0;
        pinryImages.style.textAlign = 'center';
        pinryImages.style.overflowX = 'hidden';
        pinryImages.style.overflowY = 'auto';
        var pinryBar = document.createElement('div');
        pinryBar.id = 'pinry-bar';
        pinryBar.style.background = 'black';
        pinryBar.style.padding = '15px';
        pinryBar.style.position = 'absolute';
        pinryBar.style.zIndex = 9002;
        pinryBar.style.width = '100%';
        pinryBar.style.top = 0;
        pinryBar.style.borderBottom = '1px solid #555';
        pinryBar.style.color = 'white';
        pinryBar.style.textAlign = 'center';
        pinryBar.style.fontSize = '22px';
        pinryBar.textContent = 'Pinry Bookmarklet';
        pinryBar.onclick = closePinry;
        pinryImages.appendChild(pinryBar);
        document.body.appendChild(pinryImages);
        document.onkeyup = function (e) {
            if (e.keyCode == 27) // ESC key
                closePinry();
        };
    }

    function imageView(imageUrl) {
        // Requires that pageView has been created already
        var image = document.createElement('div');
        image.style.backgroundImage = 'url('+imageUrl+')';
        image.style.backgroundPosition = 'center center';
        image.style.backgroundRepeat = 'no-repeat';
        image.style.backgroundSize = 'cover';
        image.style.display = 'inline-block';
        image.style.color = 'blue';
        image.style.textShadow = 'yellow 0px 0px 2px, yellow 0px 0px 3px, yellow 0px 0px 4px';
        image.style.width = '200px';
        image.style.height = '200px';
        image.style.margin = '15px';
        image.style.cursor = 'pointer';
        image.style.border = '1px solid #555';
        image.onclick = function() {
            var popUrl = getFormUrl()+encodeURIComponent(imageUrl);
            window.open(popUrl);
            closePinry();
        };
        document.getElementById('pinry-images').appendChild(image);
        return image;
    }
    // End View Functions


    // Start Active Functions
    function addAllImagesToPageView() {
        var images = document.getElementsByTagName('img');
        for (var i = 0; i < images.length; ++i) {
            var t = images[i],
                w = t.naturalWidth,
                h = t.naturalHeight;
            if (w > 200 && h > 200)
                imageView(t.src).textContent = w + '\u00D7' + h;
        }
        return images;
    }
    // End Active Functions


    // Start Init
    pageView(); // Build page before we insert images
    addAllImagesToPageView(); // Add all images on page to our new pageView
    // End Init
})();
