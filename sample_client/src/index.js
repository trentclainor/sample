import React from 'react';
import ReactDOM from 'react-dom';
import App from './App';
import { Provider } from 'react-redux';
import createHistory from 'history/createHashHistory';
import { ConnectedRouter } from 'react-router-redux';
import configureStore from './store/configureStore';
import { authLoginUserSuccess } from './actions/auth';
import * as axios from "axios";
import * as qs from 'qs';

const initialState = {};

const history = createHistory();
const store = configureStore(initialState, history);

const token = sessionStorage.getItem('token');
let user = {};
try {
    user = JSON.parse(sessionStorage.getItem('user'));
} catch (e) {
    // Failed to parse
}

if (token !== null) {
    store.dispatch(authLoginUserSuccess(token, user));
}

ReactDOM.render(
    <Provider store={store}>
        <ConnectedRouter history={history}>
            <App />
        </ConnectedRouter>
    </Provider>,
    document.querySelector("#app")
);

axios.defaults.paramsSerializer=function(params) {
    return qs.stringify(params, {arrayFormat: 'repeat'})
};
