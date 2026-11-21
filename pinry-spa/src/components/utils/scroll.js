import utils from './browser';

function getDocumentScrollTop() {
  const doc = document.documentElement;
  return (window.pageYOffset || doc.scrollTop) - (doc.clientTop || 0);
}

function onScroll2Bottom(callback) {
  const windowPosition = getDocumentScrollTop() + window.innerHeight;
  const bottom = utils.getDocumentHeight() - 100;
  if (windowPosition > bottom) {
    callback();
  }
}

// Returns a function that removes the listener again.
function bindScroll2Bottom(callback) {
  const listener = () => {
    onScroll2Bottom(callback);
  };
  window.addEventListener('scroll', listener, { passive: true });
  return () => window.removeEventListener('scroll', listener);
}

export default {
  bindScroll2Bottom,
};
