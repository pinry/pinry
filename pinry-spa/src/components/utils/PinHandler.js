/**
 * Remove http prefix from url.
 * @param url: String
*/
function escapeUrl(url) {
  const uri = new URL(url);
  return uri.pathname;
}


export default {
  escapeUrl,
};
