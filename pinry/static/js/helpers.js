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
    var decode = decodeURI(
        (RegExp(name + '=' + '(.+?)(&|$)').exec(location.search)||[,null])[1]
    );
    if (decode == 'null') return null;
    else return decode;
}

/*Function youtubeLinkParser parses youtube link for Video ID
based on http://stackoverflow.com/questions/3452546/javascript-regex-how-to-get-youtube-video-id-from-url 
answer #2 comment by  Chris Nolet*/
function youtubeLinkParser(youtubeUrl) {
    var regExp = /.*(?:youtu.be\/|v\/|u\/\w\/|embed\/|watch\?v=)([^#\&\?]*).*/;
    var match = youtubeUrl.match(regExp);
    if (match&&match[1].length==11){
        return match[1];
    }
    else return;
}

function vimeoLinkParser(vimeoUrl) {
    var regExp = /^.*(vimeo\.com\/)((channels\/[A-z]+\/)|(groups\/[A-z]+\/videos\/))?([0-9]+)/
    var match = /\/\/vimeo.*\/(\d+)/i.exec( vimeoUrl );
    if (match) {
        var parseUrl = regExp.exec( vimeoUrl );
        return parseUrl[5];
    } 
    else return;
}

function getVimeoThumbnail(vimeo) { 
    var thumbnail;
    $.ajax({
        url: "http://vimeo.com/api/oembed.json?url=http://vimeo.com/" + vimeo,
        async: false,
        dataType: 'json',
        success: function(data) {
            thumbnail = data.thumbnail_url;
        }
    });
    return thumbnail;
}
