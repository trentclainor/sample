import request from 'axios'
import { API_URL } from '../utils/config';
import {
    WORK_HISTORY_LIST,
    WORK_HISTORY_CREATE,
    WORK_HISTORY_UPDATE,
    WORK_HISTORY_DELETE,
    WORK_HISTORY_SHOW_EDIT_MODAL,
    WORK_HISTORY_HIDE_EDIT_MODAL
} from '../constants';

// const url = `${API_URL}/users/<userId>/job-profiles/<profileId>/work-histories/`;
const url = `${API_URL}/job-profiles/<profileId>/work-histories/`;


function prepareParams(filtering, ordering, limit, offset){
    let params = {};
    return params
}

function prepareUrl(userId, profileId) {
    let newUrl = url.replace('<userId>', userId);
    return newUrl.replace('<profileId>', profileId);
}

export function workHistoryList(userId, profileId, filtering, ordering, limit, offset) {
    let params = prepareParams(filtering, ordering, limit, offset);
    let url = prepareUrl(userId, profileId);
    return {
      type: WORK_HISTORY_LIST,
      payload: request.get(url, params)
    };
}

export function workHistoryCreate(userId, profileId, workHistory) {
    let url = prepareUrl(userId, profileId);
    return {
        type: WORK_HISTORY_CREATE,
        payload: request.post(url, workHistory)
    };
}

export function workHistoryUpdate(userId, profileId, workHistory) {
    let url = prepareUrl(userId, profileId);
    return {
      type: WORK_HISTORY_UPDATE,
      payload: request.put(`${url}${workHistory.id}/`, workHistory),
      id: workHistory.id
    }
}

export function workHistoryDelete(userId, profileId, workHistoryId) {
    let url = prepareUrl(userId, profileId);
    return {
      type: WORK_HISTORY_DELETE,
      payload: request.delete(`${url}${workHistoryId}/`, {id:workHistoryId}),
    }
}

export function showWorkHistoryEditModal(workHistory) {
    return {
      type: WORK_HISTORY_SHOW_EDIT_MODAL,
      workHistory: workHistory
    }
}
export function hideWorkHistoryEditModal() {
    return {
      type: WORK_HISTORY_HIDE_EDIT_MODAL,
    }
}
