$(document).ready(function() {
    window.message = function(text, classes) {
        classes = typeof classes !== 'undefined' ? classes : 'alert';
        messageHtml = renderTemplate('#messages-template', {
            text: text,
            classes: classes
        });
        $('#messages').append(messageHtml);
        $('#messages li').each(function() {
            $(this).delay(3000).fadeOut(300);
            var messageDelayed = $(this);
            setTimeout(function() {
                messageDelayed.remove();
            }, 3300);
        });
    }

    if (errors) {
        for (var i in errors) {
            message(errors[i].text, errors[i].tags);
        }
    }
});
