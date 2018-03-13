import request from 'axios'
import { API_URL } from '../utils/config';
import {
    BASIC_INFO_LIST,
    BASIC_INFO_CREATE,
    BASIC_INFO_UPDATE,
    BASIC_INFO_SHOW_EDIT_MODAL,
    BASIC_INFO_HIDE_EDIT_MODAL
} from '../constants';

// const url = `${API_URL}/users/<userId>/job-profiles/<profileId>/basic-info/`;
const url = `${API_URL}/job-profiles/<profileId>/basic-info/`;


function prepareParams(filtering, ordering, limit, offset){
    let params = {};
    return params
}

function prepareUrl(userId, profileId) {
    let newUrl = url.replace('<userId>', userId);
    return newUrl.replace('<profileId>', profileId);
}

export function basicInfoList(userId, profileId, filtering, ordering, limit, offset) {
    let params = prepareParams(filtering, ordering, limit, offset);
    let url = prepareUrl(userId, profileId);
    return {
      type: BASIC_INFO_LIST,
      payload: request.get(url, params)
    };
}

export function basicInfoCreate(userId, profileId, basicInfo) {
    let url = prepareUrl(userId, profileId);

    let formData = new FormData();
    Object.keys(basicInfo).forEach(key => basicInfo[key] && formData.append(key, basicInfo[key]));

    return {
        type: BASIC_INFO_CREATE,
        payload: request.post(url, formData)
    };
}

export function basicInfoUpdate(userId, profileId, basicInfo) {
    let url = prepareUrl(userId, profileId);

    let formData = new FormData();
    Object.keys(basicInfo).forEach(key => basicInfo[key] && formData.append(key, basicInfo[key]));

    return {
      type: BASIC_INFO_UPDATE,
      payload: request.put(`${url}${basicInfo.id}/`, formData),
      id: basicInfo.id
    }
}

export function showBasicInfoEditModal() {
    return {
      type: BASIC_INFO_SHOW_EDIT_MODAL,
    }
}
export function hideBasicInfoEditModal() {
    return {
      type: BASIC_INFO_HIDE_EDIT_MODAL,
    }
}
