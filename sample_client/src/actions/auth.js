import request from 'axios'
import { push } from 'react-router-redux';
import { API_URL } from '../utils/config';
import { checkHttpStatus } from '../utils';
import {
    AUTH_LOGIN_USER_REQUEST,
    AUTH_LOGIN_USER_FAILURE,
    AUTH_LOGIN_USER_SUCCESS,
    AUTH_LOGOUT_USER
} from '../constants';


export function setAxiosAuthHeader(token) {
  if (token) {
    request.defaults.headers.common['Authorization'] = `Token ${token}`
  } else {
    delete request.defaults.headers.common['Authorization']
  }
}

export function authLoginUserSuccess(token, user) {
    sessionStorage.setItem('token', token);
    sessionStorage.setItem('user', JSON.stringify(user));
    setAxiosAuthHeader(token);
    return {
        type: AUTH_LOGIN_USER_SUCCESS,
        payload: {
            token,
            user,
        }
    };
}

export function authLoginUserFailure(error, message) {
    sessionStorage.removeItem('token');
    sessionStorage.removeItem('user');
    setAxiosAuthHeader();
    return {
        type: AUTH_LOGIN_USER_FAILURE,
        payload: {
            status: error,
            statusText: message
        }
    };
}

export function authLoginUserRequest() {
    return {
        type: AUTH_LOGIN_USER_REQUEST
    };
}

export function authLogout() {
    sessionStorage.removeItem('token');
    sessionStorage.removeItem('user');
    setAxiosAuthHeader();
    return {
        type: AUTH_LOGOUT_USER
    };
}

export function authLogoutAndRedirect() {
    return (dispatch, state) => {
        dispatch(authLogout());
        dispatch(push('/login'));
    };
}

export function obtainToken(username, password) {
  const url = `${API_URL}/auth-token/`;
  return request.post(url, {username, password})
}

export function authLoginUser(email, password, redirect = '/') {
  return (dispatch) => {
      dispatch(authLoginUserRequest());
      return obtainToken(email, password)
          .then(checkHttpStatus)
          .then((response) => {
              dispatch(authLoginUserSuccess(response.data.token, response.data.user));
              dispatch(push(redirect));
          })
          .catch((error) => {
              if (error && typeof error.response !== 'undefined' && error.response.status === 401) {
                  // Invalid authentication credentials
                  return error.response.json().then((data) => {
                      dispatch(authLoginUserFailure(401, data.non_field_errors[0]));
                  });
              } else if (error && typeof error.response !== 'undefined' && error.response.status === 400) {
                  // Invalid authentication credentials
                  return error.response.json().then((data) => {
                      dispatch(authLoginUserFailure(401, data.non_field_errors[0]));
                  });
              } else if (error && typeof error.response !== 'undefined' && error.response.status >= 500) {
                  // Server side error
                  dispatch(authLoginUserFailure(500, 'A server error occurred while sending your data!'));
              } else {
                  // Most likely connection issues
                  dispatch(authLoginUserFailure('Connection Error', 'An error occurred while sending your data!'));
              }
          });
  }

}
