/* from https://github.com/liesislukas/localstorage-ttl/blob/master/index.js */
const storage = {
  set(key, value, ttlMs) {
    const data = { value, expires_at: new Date().getTime() + ttlMs / 1 };
    localStorage.setItem(key.toString(), JSON.stringify(data));
  },
  get(key) {
    const data = JSON.parse(localStorage.getItem(key.toString()));
    if (data !== null) {
      if (data.expires_at !== null && data.expires_at < new Date().getTime()) {
        localStorage.removeItem(key.toString());
      } else {
        return data.value;
      }
    }
    return null;
  },
};

export default storage;
