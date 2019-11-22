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

export default {
  fetchPins,
};
