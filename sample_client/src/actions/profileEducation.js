import request from 'axios'
import { API_URL } from '../utils/config';
import {
    EDUCATION_LIST,
    EDUCATION_CREATE,
    EDUCATION_UPDATE,
    EDUCATION_DELETE,
    EDUCATION_SHOW_EDIT_MODAL,
    EDUCATION_HIDE_EDIT_MODAL
} from '../constants';

// const url = `${API_URL}/users/<userId>/job-profiles/<profileId>/educations/`;
const url = `${API_URL}/job-profiles/<profileId>/educations/`;


function prepareParams(filtering, ordering, limit, offset){
    let params = {};
    return params
}

function prepareUrl(userId, profileId) {
    let newUrl = url.replace('<userId>', userId);
    return newUrl.replace('<profileId>', profileId);
}

export function educationList(userId, profileId, filtering, ordering, limit, offset) {
    let params = prepareParams(filtering, ordering, limit, offset);
    let url = prepareUrl(userId, profileId);
    return {
      type: EDUCATION_LIST,
      payload: request.get(url, params)
    };
}

export function educationCreate(userId, profileId, education) {
    let url = prepareUrl(userId, profileId);
    return {
        type: EDUCATION_CREATE,
        payload: request.post(url, education)
    };
}

export function educationUpdate(userId, profileId, education) {
    let url = prepareUrl(userId, profileId);
    return {
      type: EDUCATION_UPDATE,
      payload: request.put(`${url}${education.id}/`, education),
      id: education.id
    }
}

export function educationDelete(userId, profileId, educationId) {
    let url = prepareUrl(userId, profileId);
    return {
      type: EDUCATION_DELETE,
      payload: request.delete(`${url}${educationId}/`, {id:educationId}),
    }
}

export function showEducationEditModal(education) {
    return {
      type: EDUCATION_SHOW_EDIT_MODAL,
      education: education
    }
}
export function hideEducationEditModal() {
    return {
      type: EDUCATION_HIDE_EDIT_MODAL,
    }
}
