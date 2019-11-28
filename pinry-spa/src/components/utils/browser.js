const utils = {
  getDocumentHeight() {
    const html = document.documentElement;
    return Math.max(
      document.body.scrollHeight, document.body.offsetHeight,
      html.clientHeight, html.scrollHeight,
      html.offsetHeight,
    );
  },
  getWindowHeight() {
    return window.innerHeight;
  },
};

export default utils;
