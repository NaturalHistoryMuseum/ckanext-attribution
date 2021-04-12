import axios from 'axios';
import axiosCancel from 'axios-cancel';

const api = axios.create({
    baseURL: '/api/3/action/',
    timeout: 60000,
    headers: {
        'Content-Type': 'application/json'
    }
});

axiosCancel(api, {debug: false});

export const cancelAll = api.cancelAll;


export function post(action, body, requestId) {
    return api.post(action, body, {requestId: requestId})
              .then(response => {
                  if (response.data && response.data.success) {
                      return response.data.result;
                  } else {
                      throw Error(response.data.error || 'Unspecified error');
                  }
              })
              .catch(e => {
                  // console.error(e);
              });
}

export function get(action, requestId) {
    return api.get(action, {requestId: requestId})
              .then(response => {
                  if (response.data && response.data.success) {
                      return response.data.result;
                  } else {
                      throw Error(response.data.error || 'Unspecified error');
                  }
              })
              .catch(e => {
                  // console.error(e);
              });
}