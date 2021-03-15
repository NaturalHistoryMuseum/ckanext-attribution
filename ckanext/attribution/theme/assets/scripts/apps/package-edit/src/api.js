import axios from 'axios';
import axiosCancel from 'axios-cancel';

const api = axios.create({
                             baseURL: '/api/3/action/',
                             timeout: 60000,
                             headers: {
                                 'Content-Type': 'application/json'
                             }
                         });

axiosCancel(api, {debug: false})


export function post(action, body, requestId) {
    return api.post(action, body, {requestId: requestId})
              .then(response => {
                  return response.data;
              });
}

export function get(action, requestId) {
    return api.get(action, {requestId: requestId})
              .then(response => {
                  return response.data;
              })
}