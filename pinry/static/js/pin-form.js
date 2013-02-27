/**
 * Pin Form for Pinry
 * Descrip: This is for creation new pins on everything, the bookmarklet, on the
 *          site and even editing pins in some limited situations.
 * Authors: Pinry Contributors
 * Updated: Feb 27th, 2013
 * Require: jQuery, Pinry JavaScript Helpers
 */


$(window).load(function() {
    var currentPin;
    // Start Helper Functions
    function getFormData() {
        return {
            submitter: currentUser,
            url: $('#pin-form-image-url').val(),
            description: $('#pin-form-description').val(),
            tags: cleanTags($('#pin-form-tags').val())
        }
    }

    function createPinPreviewFromForm() {
        var context = {pins: [{
                submitter: currentUser,
                image: {thumbnail: {image: $('#pin-form-image-url').val()}},
                description: $('#pin-form-description').val(),
                tags: cleanTags($('#pin-form-tags').val())
            }]},
            html = renderTemplate('#pins-template', context),
            preview = $('#pin-form-image-preview');
        preview.html(html);
        preview.find('.pin').width(200);
        preview.find('.pin .text').width(140);
        if (preview.height() > 305)
            $('#pin-form .modal-body').height(preview.height());
    }

    function dismissModal(modal) {
        modal.modal('hide');
        setTimeout(function() {
            modal.remove();
        }, 200);
    }
    // End Helper Functions


    // Start View Functions
    function createPinForm() {
        $('body').append(renderTemplate('#pin-form-template', ''));
        var modal = $('#pin-form'),
            formFields = [$('#pin-form-image-url'), $('#pin-form-description'),
            $('#pin-form-tags')],
            pinFromUrl = getUrlParameter('pin-image-url');
        modal.modal('show');
        for (var i in formFields) {
            formFields[i].bind('propertychange keyup input paste', function() {
                createPinPreviewFromForm()
            });
        }
        if (pinFromUrl) {
            $('#pin-form-image-url').val(pinFromUrl);
            $('.navbar').css('display', 'none');
            modal.css({
                'margin-top': -35,
                'margin-left': -281
            });
        }
        $('#pin-form-submit').click(function(e) {
            e.preventDefault();
            var data = {
                    submitter: '/api/v1/user/'+currentUser.id+'/',
                    url: $('#pin-form-image-url').val(),
                    description: $('#pin-form-description').val(),
                    tags: cleanTags($('#pin-form-tags').val())
                },
                promise = postPinData(data);
            promise.success(function() {
                if (pinFromUrl) return window.close();
                $('#pins').prepend(currentPin);
                dismissModal(modal);
            });

        });
        $('#pin-form-close').click(function() {
            if (pinFromUrl) return window.close();
            dismissModal(modal);
        });
        createPinPreviewFromForm();
    }
    // End View Functions


    // Start Init
    window.pinForm = function() {
        createPinForm();
    }

    if (getUrlParameter('pin-image-url')) {
        createPinForm();
    }
    // End Init
});
