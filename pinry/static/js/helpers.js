/**
 * Helpers for Pinry
 * Descrip: A hodgepodge of useful things to help clean up Pinry's JavaScript.
 * Authors: Pinry Contributors
 * Updated: Feb 26th, 2013
 * Require: jQuery
 */
var API_BASE = "/api/v2/";


function _getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


function getCSRFToken() {
    return _getCookie('csrftoken');
}


function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", getCSRFToken());
        }
    }
});


function renderTemplate(templateId, context) {
    var template = Handlebars.compile($(templateId).html());
    return template(context);
}


function cleanTags(tags) {
    if (typeof tags === 'string' && tags.length > 0) {
        tags = tags.split(/[\s,]+/);
        for (var i in tags) {
            tags[i] = tags[i].trim();
        }
    } else {
        return [];
    }
    return tags;
}

function getPinData(pinId) {
    var apiUrl = API_BASE + "pins/" + pinId + '/?format=json';
    return $.get(apiUrl);
}


function deletePinData(pinId) {
    var apiUrl = API_BASE + 'pins/' +pinId + '/?format=json';
    return $.ajax(apiUrl, {
        type: 'DELETE'
    });
}

function postPinData(data) {
    return $.ajax({
        type: "post",
        url: API_BASE + "pins/",
        contentType: 'application/json',
        data: JSON.stringify(data)
    });
}


function getUrlParameter(name) {
    return decodeURIComponent((new RegExp('[?|&]' + name + '=' + '([^&;]+?)(&|#|;|$)').exec(location.search)||[,""])[1].replace(/\+/g, '%20'))||null;
}

Handlebars.registerHelper('niceLinks', (function () {
    var reNL = /\r?\n/g,
        reURL = /https?:[/][/](?:www[.])?([^/]+)(?:[/]([.]?[^\s,.])+)?/g;
    return function (text) {
        var t = Handlebars.Utils.escapeExpression(text);
        t = t.replace(reURL, '<a href="$&" target="_blank">$1</a>');
        t = t.replace(reNL, '<br>');
        return new Handlebars.SafeString(t);
    };
})());

