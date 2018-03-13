import request from 'axios'
import { API_URL } from '../utils/config';
import {
    VACANCY_LIST,
    VACANCY_CREATE,
    VACANCY_UPDATE,
    VACANCY_DELETE,
    APPLY_SEARCH_FILTERS,
    VACANCY_STANDARD_SEARCH,
    VACANCY_PERSONALIZED_SEARCH
} from '../constants';
import {prepareParams} from '../utils';

const url = `${API_URL}/vacancies/`;
// standard
// personalized
const searchUrl = `${API_URL}/search/vacancies/`;

export function getList(filtering, ordering, limit, offset) {
    let params = prepareParams(filtering, ordering, limit, offset);
    return {
        type: VACANCY_LIST,
        payload: request.get(url, {params: params})
    };
}

export function createItem(item) {
    let formData = new FormData();
    Object.keys(item).forEach(key => item[key] && formData.append(key, item[key]));

    return {
        type: VACANCY_CREATE,
        payload: request.post(url, formData)
    };
}

export function updateItem(item) {
    let formData = new FormData();
    Object.keys(item).forEach(key => item[key] && formData.append(key, item[key]));

    return {
        type: VACANCY_UPDATE,
        payload: request.put(`${url}${item.id}/`, formData),
        id: item.id
    }
}

export function deleteItem(itemId) {
    return {
        type: VACANCY_DELETE,
        payload: request.delete(`${url}${itemId}/`, {id: itemId}),
    }
}

export function applyFilters(filters) {
    return {
        type: APPLY_SEARCH_FILTERS,
        payload: filters
    };
}

export function standardSearch(filtering, ordering, limit, offset) {
    let params = prepareParams(filtering, ordering, limit, offset);
    let url = searchUrl + 'standard/';
    return {
        type: VACANCY_STANDARD_SEARCH,
        payload: request.get(url, {params: params})
    };
}

export function personalizedSearch(filtering, ordering, limit, offset) {
    let params = prepareParams(filtering, ordering, limit, offset);
    let url = searchUrl + 'personalized/';
    return {
        type: VACANCY_PERSONALIZED_SEARCH,
        payload: request.get(url, {params: params})
    };
}

