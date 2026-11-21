const entities = {
  '&': '&amp;',
  '<': '&lt;',
  '>': '&gt;',
  '"': '&quot;',
  "'": '&#39;',
};
function escapeHTML(text) {
  return text.replace(/[&<>"']/g, c => entities[c]);
}

// Quotes and angle brackets end a URL, so a match can't break out of href.
const reURL = /https?:[/][/](?:www[.])?([^/\s"'<>]+)(?:[/]([.]?[^\s,.<>"'])+)?/g;
function niceLinks(text) {
  if (!text) return '';
  let html = '';
  let last = 0;
  text.replace(reURL, (url, host, ...rest) => {
    const offset = rest[rest.length - 2];
    html += escapeHTML(text.slice(last, offset));
    html += `<a href="${escapeHTML(url)}" target="_blank" rel="noopener noreferrer">${escapeHTML(host)}</a>`;
    last = offset + url.length;
    return url;
  });
  return html + escapeHTML(text.slice(last));
}

export default niceLinks;
