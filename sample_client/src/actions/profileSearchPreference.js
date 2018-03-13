import request from 'axios'
import { API_URL } from '../utils/config';
import {
    SEARCH_PREFERENCE_LIST,
    SEARCH_PREFERENCE_CREATE,
    SEARCH_PREFERENCE_UPDATE,
} from '../constants';

// const url = `${API_URL}/users/<userId>/job-profiles/<profileId>/preferences/`;
const url = `${API_URL}/job-profiles/<profileId>/preferences/`;


function prepareParams(filtering, ordering, limit, offset){
    let params = {};
    return params
}

function prepareUrl(userId, profileId) {
    let newUrl = url.replace('<userId>', userId);
    return newUrl.replace('<profileId>', profileId);
}

export function preferenceList(userId, profileId, filtering, ordering, limit, offset) {
    let params = prepareParams(filtering, ordering, limit, offset);
    let url = prepareUrl(userId, profileId);
    return {
      type: SEARCH_PREFERENCE_LIST,
      payload: request.get(url, params)
    };
}

export function preferenceCreate(userId, profileId, preference) {
    let url = prepareUrl(userId, profileId);
    return {
        type: SEARCH_PREFERENCE_CREATE,
        payload: request.post(url, preference)
    };
}

export function preferenceUpdate(userId, profileId, preference) {
    let url = prepareUrl(userId, profileId);
    return {
      type: SEARCH_PREFERENCE_UPDATE,
      payload: request.put(`${url}${preference.id}/`, preference),
      id: preference.id
    }
}
