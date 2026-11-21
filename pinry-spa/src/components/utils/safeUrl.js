/**
 * Return url only if it is an http(s) link, otherwise null.
 * Guards hrefs built from user input against javascript: and data: URLs.
 * @param url: String
*/
function safeUrl(url) {
  if (!url) return null;
  try {
    const { protocol } = new URL(url, window.location.href);
    if (protocol === 'http:' || protocol === 'https:') return url;
  } catch (e) {
    // invalid URL, fall through
  }
  return null;
}

export default safeUrl;
