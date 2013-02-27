$(window).load(function() {
    var currentPin;

    function createPin() {
        var template = Handlebars.compile($('#pins-template').html());
        var html = template({
            pins: [{
                submitter: currentUser,
                image: {
                    standard: {
                        image: $('#pin-form-image-url').val()
                    },
                    thumbnail: {
                        image: $('#pin-form-image-url').val()
                    }
                },
                description: $('#pin-form-description').val(),
                tags: cleanTags($('#pin-form-tags').val())
            }]
        });
        currentPin = html;
        return html
    }

    function createPreview() {
        $('#pin-form-image-preview').html(createPin());
        $('#pin-form-image-preview .pin').css('width', '200px');
        $('#pin-form-image-preview .pin .text').css('width', '140px');
        var pinHeight = $('#pin-form-image-preview .pin').height();
        if (pinHeight > 305)
            $('#pin-form .modal-body').css('height', String(pinHeight)+'px');
    }

    function createPinForm() {
        var template = Handlebars.compile($('#pin-form-template').html());
        var html = template();
        $('body').append(html);
        $('#pin-form-image-url').bind('propertychange keyup input paste', function() {
            createPreview();
        });
        $('#pin-form-description').bind('propertychange keyup input paste', function() {
            createPreview();
        });
        $('#pin-form-tags').bind('propertychange keyup input paste', function() {
            createPreview();
        });

        function getURLParameter(name) {
            return decodeURI(
                (RegExp(name + '=' + '(.+?)(&|$)').exec(location.search)||[,null])[1]
            );
        }
        if (getURLParameter('pin-image-url') != 'null') {
            $('#pin-form-image-url').val(getURLParameter('pin-image-url'));
            createPreview();
        }

        $('#pin-form-submit').click(function(e) {
            var tags = cleanTags($('#pin-form-tags').val());
            $.ajax({
                type: "post",
                url: "/api/v1/pin/",
                contentType: 'application/json',
                data: JSON.stringify({
                    submitter: '/api/v1/user/'+currentUser.id+'/',
                    url: $('#pin-form-image-url').val(),
                    description: $('#pin-form-description').val(),
                    tags: tags
                }),
                success: function() {
                    $('#pins').prepend(currentPin);
                },
                error: function() {
                    alert("Something went wrong. :(");
                }
            });

            $('#pin-form-close').click(function() {
                $('#pin-form').remove();
            });

            $('#pin-form').remove();

            e.preventDefault();
        });

        $('#pin-form-close').click(function() {
            $('#pin-form').remove();
        });
    }

    if ($('#display-pin-form').length >= 1) createPinForm();

    $('#call-pin-form').click(function() {
        createPinForm();
    });
});
