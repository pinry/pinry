import axios from 'axios';
import storage from './utils/storage';

const api = axios.create({
  responseType: 'json',
  transitional: {
    silentJSONParsing: false
  },
  baseURL: '/api/v2/'
})

const Board = {
  create(name, private_ = false) {
    const data = { name, private: private_ };
    return new Promise(
      (resolve, reject) => {
        api.post('boards', data).then(
          (resp) => {
            if (resp.status !== 201) {
              reject(resp);
            }
            resolve(resp.data);
          },
          (error) => {
            reject(error.response);
          },
        );
      },
    );
  },
  get(boardId) {
    return api.get(`boards/${boardId}`);
  },
  fetchFullList(username) {
    return api.get(`boards-auto-complete/?submitter__username=${username}`);
  },
  fetchSiteFullList() {
    return api.get(`boards-auto-complete`);
  },
  fetchListWhichContains(text, offset = 0, limit = 50) {
    return api.get(`boards/?search=${text}&offset=${offset}&limit=${limit}`);
  },
  saveChanges(boardId, fieldsForm) {
    return api.patch(
      `boards/${boardId}`,
      fieldsForm,
    );
  },
  addToBoard(boardId, pinIds) {
    return api.patch(
      `boards/${boardId}`,
      { pins_to_add: pinIds },
    );
  },
  removeFromBoard(boardId, pinIds) {
    return api.patch(
     `boards/${boardId}`,
      { pins_to_remove: pinIds },
    );
  },
  delete(boardId) {
    return api.delete(`boards/${boardId}`);
  },
};

const Pin = {
  create(jsonData) {
    return api.post(
     `pins`,
      jsonData
    );
  },
  createFromURL(jsonData) {
    return this.create(jsonData);
  },
  createFromUploaded(jsonData) {
    return this.create(jsonData);
  },
  uploadImage(fileObject) {
    const data = new FormData();
    data.append('image', fileObject);
    return api.post(
      `images`,
      data,
      {
        headers: {
          'Content-Type': 'multipart/form-data',
        }
      }
    );
  },
  deleteById(pinId) {
    return api.delete(`pins/${pinId}`);
  },
  updateById(pinId, data) {
    return api.patch(
      `pins/${pinId}`,
      data
    );
  },
};


function fetchPins(offset, tagFilter, userFilter, boardFilter) {
  const queryArgs = {
    format: 'json',
    ordering: '-id',
    limit: 30,
    offset
  };
  if (tagFilter) queryArgs.tags__name = tagFilter;
  if (userFilter) queryArgs.submitter__username = userFilter;
  if (boardFilter) queryArgs.pins__id = boardFilter;
  return api.get(
    `pins`,
    { params: queryArgs }
  );
}

function fetchPin(pinId) {
  return new Promise(
    (resolve, reject) => {
      const p = api.get(`pins/${pinId}`);
      p.then(
        (resp) => {
          const response = {
            data: { results: [resp.data], next: null },
          };
          resolve(response);
        },
        (error) => {
          reject(error);
        },
      );
    },
  );
}

function fetchBoardForUser(username, offset = 0, limit = 50) {
  return api.get(`boards/?submitter__username=${username}&offset=${offset}&limit=${limit}`);
}

const User = {
  storageKey: 'pinry.user',
  signUp(username, email, password, passwordRepeat) {
    return new Promise(
      (resolve, reject) => {
        const p = api.post(
          `profile/users`,
          {
            username,
            email,
            password,
            password_repeat: passwordRepeat
          },
        );
        p.then(
          (resp) => {
            if (resp.status !== 201) {
              reject(resp);
            }
            resolve(resp.data);
          },
          (error) => {
            console.log('Failed to sign up due to unexpected error:', error);
            reject(error.response);
          }
        );
      },
    );
  },
  logIn(username, password) {
    return new Promise(
      (resolve, reject) => {
        const p = api.post(
          `profile/login`,
          {
            username,
            password
          }
        );
        p.then(
          (resp) => {
            if (resp.status !== 200) {
              reject(resp);
            }
            resolve(resp.data);
          },
          (error) => {
            console.log('Failed to log in due to unexpected error:', error);
            reject(error.response);
          }
        );
      },
    );
  },
  logOut() {
    const self = this;
    return new Promise(
      (resolve) => {
        api.get('/api-auth/logout').then(
          () => {
            storage.set(self.storageKey, null, 1);
            resolve();
          }
        );
      },
    );
  },
  fetchUserInfoByName(username) {
    /* returns null if user not logged in */
    return new Promise(
      (resolve) => {
        api.get(`profile/public-users/?username=${username}`).then(
          (resp) => {
            const users = resp.data;
            if (users.length === 0) {
              return resolve(null);
            }
            return resolve(users[0]);
          }
        );
      },
    );
  },
  fetchUserInfo(force = false) {
    /* returns null if user not logged in */
    const self = this;
    if (!force) {
      const userInfo = storage.get(self.storageKey);
      if (userInfo !== null) {
        return new Promise(
          resolve => resolve(userInfo)
        );
      }
    }
    return new Promise(
      (resolve) => {
        api.get(`profile/users`).then(
          (resp) => {
            const users = resp.data;
            if (users.length === 0) {
              return resolve(null);
            }
            const value = users[0];
            storage.set(self.storageKey, value, 60 * 5 * 1000);
            return resolve(users[0]);
          }
        );
      },
    );
  },
};

const Tag = {
  fetchList() {
    return api.get(`tags-auto-complete`);
  },
};

export default {
  Tag,
  Pin,
  Board,
  fetchPin,
  fetchPins,
  fetchBoardForUser,
  User,
};
