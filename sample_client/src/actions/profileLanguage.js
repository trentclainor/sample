import request from 'axios'
import { API_URL } from '../utils/config';
import {
    LANGUAGE_LIST,
    LANGUAGE_CREATE,
    LANGUAGE_UPDATE,
    LANGUAGE_DELETE,
    LANGUAGE_SHOW_EDIT_MODAL,
    LANGUAGE_HIDE_EDIT_MODAL
} from '../constants';

// const url = `${API_URL}/users/<userId>/job-profiles/<profileId>/languages/`;
const url = `${API_URL}/job-profiles/<profileId>/languages/`;


function prepareParams(filtering, ordering, limit, offset){
    let params = {};
    return params
}

function prepareUrl(userId, profileId) {
    let newUrl = url.replace('<userId>', userId);
    return newUrl.replace('<profileId>', profileId);
}

export function languageList(userId, profileId, filtering, ordering, limit, offset) {
    let params = prepareParams(filtering, ordering, limit, offset);
    let url = prepareUrl(userId, profileId);
    return {
      type: LANGUAGE_LIST,
      payload: request.get(url, params)
    };
}

export function languageCreate(userId, profileId, language) {
    let url = prepareUrl(userId, profileId);
    return {
        type: LANGUAGE_CREATE,
        payload: request.post(url, language)
    };
}

export function languageUpdate(userId, profileId, language) {
    let url = prepareUrl(userId, profileId);
    return {
      type: LANGUAGE_UPDATE,
      payload: request.put(`${url}${language.id}/`, language),
      id: language.id
    }
}

export function languageDelete(userId, profileId, languageId) {
    let url = prepareUrl(userId, profileId);
    return {
      type: LANGUAGE_DELETE,
      payload: request.delete(`${url}${languageId}/`, {id:languageId}),
    }
}

export function showLanguageEditModal(language) {
    return {
      type: LANGUAGE_SHOW_EDIT_MODAL,
      language: language
    }
}
export function hideLanguageEditModal() {
    return {
      type: LANGUAGE_HIDE_EDIT_MODAL,
    }
}
