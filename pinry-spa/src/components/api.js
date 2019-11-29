import axios from 'axios';
import storage from './utils/storage';

const API_PREFIX = '/api/v2/';

function fetchPins(offset, tagFilter, userFilter) {
  const url = `${API_PREFIX}pins/`;
  const queryArgs = {
    format: 'json',
    ordering: '-id',
    limit: 30,
    offset,
  };
  if (tagFilter) queryArgs.tags__name = tagFilter;
  if (userFilter) queryArgs.submitter__username = userFilter;
  return axios.get(
    url,
    { params: queryArgs },
  );
}

function fetchPinsForBoard(boardId) {
  const url = `${API_PREFIX}boards/${boardId}`;
  return new Promise(
    (resolve, reject) => {
      axios.get(url).then(
        (resp) => {
          resolve({ data: { results: resp.data.pins_detail, next: null } });
        },
        error => reject(error),
      );
    },
  );
}

const User = {
  storageKey: 'pinry.user',
  logOut() {
    const self = this;
    return new Promise(
      (resolve) => {
        axios.get('/api-auth/logout/?next=/api/v2/').then(
          () => {
            storage.set(self.storageKey, null, 1);
            resolve();
          },
        );
      },
    );
  },
  fetchUserInfo() {
    /* returns null if user not logged in */
    const self = this;
    const userInfo = storage.get(self.storageKey);
    if (userInfo !== null) {
      return new Promise(
        resolve => resolve(userInfo),
      );
    }
    const url = `${API_PREFIX}users/`;
    return new Promise(
      (resolve) => {
        axios.get(url).then(
          (resp) => {
            const users = resp.data;
            if (users.length === 0) {
              return resolve(null);
            }
            const value = users[0];
            storage.set(self.storageKey, value, 60 * 5 * 1000);
            return resolve(users[0]);
          },
        );
      },
    );
  },
};

export default {
  fetchPins,
  fetchPinsForBoard,
  User,
};
