import axios from 'axios';

const API_PREFIX = '/api/v2/';

function fetchPins(offset, tagFilter, userFilter) {
  const url = `${API_PREFIX}pins/`;
  const queryArgs = {
    format: 'json',
    ordering: '-id',
    limit: 50,
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
          resolve({ data: { results: resp.data.pins_detail } });
        },
        error => reject(error),
      );
    },
  );
}

export default {
  fetchPins,
  fetchPinsForBoard,
};
