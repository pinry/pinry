import axios from 'axios';

function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) {
    return parts.pop().split(';').shift();
  }
  return null;
}


function getCSRFToken() {
  return getCookie('csrftoken');
}

function csrfSafeMethod(method) {
  // these HTTP methods do not require CSRF protection
  return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function setUpAxiosCsrfConfig() {
  axios.interceptors.request.use(
    (config) => {
      if (!csrfSafeMethod(config.method.toUpperCase())) {
        // eslint-disable-next-line no-param-reassign
        config.headers['X-CSRFToken'] = getCSRFToken();
      }
      return config;
    },
    (error) => {
      Promise.reject(error);
    },
  );
}

export default setUpAxiosCsrfConfig;
