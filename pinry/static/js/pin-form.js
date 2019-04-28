/**
 * Pin Form for Pinry
 * Descrip: This is for creation new pins on everything, the bookmarklet, on the
 *          site and even editing pins in some limited situations.
 * Authors: Pinry Contributors
 * Updated: March 3rd, 2013
 * Require: jQuery, Pinry JavaScript Helpers
 */


$(window).load(function() {
    var uploadedImage = false;
    var editedPin = null;

    // Start Helper Functions
    function getFormData() {
        return {
            url: $('#pin-form-image-url').val(),
            referer: $('#pin-form-referer').val(),
            description: $('#pin-form-description').val(),
            tags: cleanTags($('#pin-form-tags').val())
        }
    }

    function createPinPreviewFromForm() {
        var context = {pins: [{
                image: {thumbnail: {image: $('#pin-form-image-url').val()}},
                referer: $('#pin-form-referer').val(),
                description: $('#pin-form-description').val(),
                tags: cleanTags($('#pin-form-tags').val()),
                submitter: currentUser,
            }]},
            html = renderTemplate('#pins-template', context),
            preview = $('#pin-form-image-preview');
        preview.html(html);
        preview.find('.pin').width(240);
        preview.find('.pin').fadeIn(300);
        if (getFormData().url == "")
            preview.find('.image-wrapper').height(255);
        preview.find('.image-wrapper img').fadeIn(300);
        setTimeout(function() {
            if (preview.find('.pin').height() > 305) {
                $('#pin-form .modal-body').animate({
                    'height': preview.find('.pin').height()+25
                }, 300);
            }
        }, 300);
    }

    function dismissModal(modal) {
        modal.modal('hide');
        modal.on('hidden.bs.modal', function() {
            modal.remove();
        });
    }
    // End Helper Functions


    // Start View Functions
    function createPinForm(editPinId) {
        $('body').append(renderTemplate('#pin-form-template', ''));
        var modal = $('#pin-form'),
            formFields = [
              $('#pin-form-image-url'),
              $('#pin-form-referer'),
              $('#pin-form-description'),
              $('#pin-form-tags')
            ],
            pinFromUrl = getUrlParameter('pin-image-url'),
            pinFromDescription = getUrlParameter('description'),
            pinFromReferer = getUrlParameter('referer');
        // If editable grab existing data
        if (editPinId) {
            var promise = getPinData(editPinId);
            promise.success(function(data) {
                editedPin = data;
                $('#pin-form-image-url').val(editedPin.image.thumbnail.image);
                $('#pin-form-image-url').parent().hide();
                $('#pin-form-referer').parent().hide();
                $('#pin-form-image-upload').parent().hide();
                $('#pin-form-description').val(editedPin.description);
                $('#pin-form-tags').val(editedPin.tags);
                createPinPreviewFromForm();
            });
        }
        modal.modal('show');
        // Auto update preview on field changes
        var timer;
        for (var i in formFields) {
            formFields[i].bind('propertychange keyup input paste', function() {
                clearTimeout(timer);
                timer = setTimeout(function() {
                    createPinPreviewFromForm()
                }, 700);
                if (!uploadedImage)
                    $('#pin-form-image-upload').parent().fadeOut(300);
            });
        }
        // Drag and drop upload
        $('#pin-form-image-upload').dropzone({
            url: API_BASE + "images/",
            paramName: 'image',
            parallelUploads: 1,
            uploadMultiple: false,
            maxFiles: 1,
            acceptedFiles: 'image/*',
            headers: {
                'X-CSRFToken': getCSRFToken(),
            },
            success: function(file, resp) {
                var image_url = $('#pin-form-image-url');
                image_url.parent().fadeOut(300);
                uploadedImage = resp.id;
                image_url.val(resp.thumbnail.image);
                createPinPreviewFromForm();
            },
            error: function (error) {
              message('Problem uploading image.', 'alert alert-error');
            },
        });
        // If bookmarklet submit
        if (pinFromUrl) {
            $('#pin-form-image-upload').parent().css('display', 'none');
            $('#pin-form-image-url').val(pinFromUrl);
            $('#pin-form-referer').val(pinFromReferer);
            $('#pin-form-description').val(pinFromDescription);
            $('.navbar').css('display', 'none');
            modal.css({
                'margin-top': -35,
                'margin-left': -281
            });
        }
        // Submit pin on post click
        $('#pin-form-submit').click(function(e) {
            e.preventDefault();
            $(this).off('click');
            $(this).addClass('disabled');
            if (editedPin) {
                var apiUrl = API_BASE + 'pins/' + editedPin.id + '/?format=json';
                var data = {
                    description: $('#pin-form-description').val(),
                    tags: cleanTags($('#pin-form-tags').val())
                };
                var promise = $.ajax({
                    type: "patch",
                    url: apiUrl,
                    contentType: 'application/json',
                    data: JSON.stringify(data)
                });
                promise.success(function(pin) {
                    pin.editable = true;
                    var renderedPin = renderTemplate('#pins-template', {
                        pins: [
                            pin
                        ]
                    });
                    $('#pins').find('.pin[data-id="'+pin.id+'"]').replaceWith(renderedPin);
                    tileLayout();
                    lightbox();
                    dismissModal(modal);
                    editedPin = null;
                });
                promise.error(function() {
                    message('Problem updating image.', 'alert alert-danger');
                });
            } else {
                var data = {
                    referer: $('#pin-form-referer').val(),
                    description: $('#pin-form-description').val(),
                    tags: cleanTags($('#pin-form-tags').val())
                };
                if (uploadedImage) {
                    data.image_by_id = uploadedImage;
                } else {
                    data.url = $('#pin-form-image-url').val();
                }
                var promise = postPinData(data);
                promise.success(function(pin) {
                    if (pinFromUrl) return window.close();
                    pin.editable = true;
                    pin = renderTemplate('#pins-template', {pins: [pin]});
                    $('#pins').prepend(pin);
                    tileLayout();
                    lightbox();
                    dismissModal(modal);
                    uploadedImage = false;
                });
                promise.error(function() {
                    message('Problem saving image.', 'alert alert-danger');
                });
            }
        });
        $('#pin-form-close').click(function() {
            if (pinFromUrl) return window.close();
            dismissModal(modal);
        });
        createPinPreviewFromForm();
    }
    // End View Functions


    // Start Init
    window.pinForm = function(editPinId) {
        editPinId = typeof editPinId !== 'undefined' ? editPinId : null;
        createPinForm(editPinId);
    }

    if (getUrlParameter('pin-image-url')) {
        createPinForm();
    }
    // End Init
});
