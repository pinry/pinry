/**
 * Helpers for Pinry
 * Descrip: A hodgepodge of useful things to help clean up Pinry's JavaScript.
 * Authors: Pinry Contributors
 * Updated: Feb 26th, 2013
 * Require: jQuery
 */


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


function getImageData(imageId) {
    var apiUrl = '/api/v1/image/'+imageId+'/?format=json';
    return $.get(apiUrl);
}


function getPinData(pinId) {
    var apiUrl = '/api/v1/pin/'+pinId+'/?format=json';
    return $.get(apiUrl);
}


function deletePinData(pinId) {
    var apiUrl = '/api/v1/pin/'+pinId+'/?format=json';
    return $.ajax(apiUrl, {
        type: 'DELETE'
    });
}

function postPinData(data) {
    return $.ajax({
        type: "post",
        url: "/api/v1/pin/",
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

