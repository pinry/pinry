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
    if (typeof tags === 'string') {
        tags = tags.split(',');
        for (var i in tags) tags[i] = tags[i].trim();
    }
    return tags
}


function getPinData(pinId) {
    var apiUrl = '/api/v1/pin/'+pinId+'/?format=json';
    return $.get(apiUrl);
}
