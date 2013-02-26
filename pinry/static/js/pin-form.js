$(window).load(function() {
    function createPinForm() {
        var template = Handlebars.compile($('#pin-form-template').html());
        var html = template();
        $('body').append(html);
        $('#pin-form-image-url').bind('propertychange keyup input paste', function() {
            $('#pin-form-image-preview').html('<img src="'+$(this).val()+'"/>');
        });
        $('#pin-form-submit').click(function(e) {
            var tags = $('#pin-form-tags').val()
            tags = tags.split(',')
            for (var tag in tags) tags[tag] = tags[tag].trim();
            $.ajax({
                type: "post",
                url: "/api/v1/pin/",
                contentType: 'application/json',
                data: JSON.stringify({
                    submitter: '/api/v1/user/'+currentUser+'/',
                    url: $('#pin-form-image-url').val(),
                    description: $('#pin-form-description').val(),
                    tags: tags
                })
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
        e.preventDefault();
    }

    $('#call-pin-form').click(function() {
        createPinForm();
    });
});
