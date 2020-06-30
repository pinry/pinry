const encoder = document.createElement('div');
function escapeHTML(text) {
  encoder.innerText = text;
  return encoder.innerHTML;
}

const reURL = /https?:[/][/](?:www[.])?([^/]+)(?:[/]([.]?[^\s,.<>])+)?/g;
function niceLinks(text) {
  if (!text) return '';
  return escapeHTML(text).replace(reURL, '<a href="$&" target="_blank">$1</a>');
}

export default niceLinks;
