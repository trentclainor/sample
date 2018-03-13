import request from 'axios'
import { API_URL } from '../utils/config';
import {
    JOB_PROFILE_LIST,
    JOB_PROFILE_CREATE,
    JOB_PROFILE_UPDATE,
    JOB_PROFILE_MARK_DEFAULT,
    JOB_PROFILE_DELETE,
    JOB_PROFILE_SHOW_EDIT_MODAL,
    JOB_PROFILE_HIDE_EDIT_MODAL,
    JOB_PROFILE_SELECT
} from '../constants';

const url = `${API_URL}/job-profiles/`;


function prepareParams(filtering, ordering, limit, offset){
    let params = {};
    return params
}

export function jobProfileList(filtering, ordering, limit, offset) {
    let params = prepareParams(filtering, ordering, limit, offset);
    return {
      type: JOB_PROFILE_LIST,
      payload: request.get(url, params)
    };
}

export function jobProfileCreate(profile) {
    let formData = new FormData();
    Object.keys(profile).forEach(key => profile[key] && formData.append(key, profile[key]));

    return {
        type: JOB_PROFILE_CREATE,
        payload: request.post(url, formData)
    };
}

export function jobProfileUpdate(profile) {
    let formData = new FormData();
    Object.keys(profile).forEach(key => profile[key] && formData.append(key, profile[key]));

    return {
      type: JOB_PROFILE_UPDATE,
      payload: request.put(`${url}${profile.id}/`, formData),
      id: profile.id
    }
}

export function jobProfileMarkDefault(profileId) {
    return {
      type: JOB_PROFILE_MARK_DEFAULT,
      payload: request.post(`${url}${profileId}/make_default/`),
    }
}

export function jobProfileDelete(profileId) {
    return {
      type: JOB_PROFILE_DELETE,
      payload: request.delete(`${url}${profileId}/`, {id:profileId}),
    }
}

export function showJobProfileEditModal(jobProfile) {
    return {
      type: JOB_PROFILE_SHOW_EDIT_MODAL,
      jobProfile: jobProfile
    }
}
export function hideJobProfileEditModal() {
    return {
      type: JOB_PROFILE_HIDE_EDIT_MODAL,
    }
}

export function selectJobProfile(profile) {
    return {
      type: JOB_PROFILE_SELECT,
      profile: profile
    }
}
