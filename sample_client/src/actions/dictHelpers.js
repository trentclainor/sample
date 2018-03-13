import request from 'axios'
import { API_URL } from '../utils/config';
import {
    LOOKING_FOR_LIST,
    LOCATION_LIST,
    INDUSTRY_LIST,
    ROLE_LIST,
    COUNTRY_LIST,
    STATE_LIST,
    CITY_LIST
} from '../constants';

const commonUrl = `${API_URL}/common/`;
const dictUrl = `${API_URL}/choices/`;


function prepareParams(filtering, ordering, limit, offset){
    return {
        limit: 1000,
    }
}

export function lookingForList(filtering, ordering, limit, offset) {
    let params = prepareParams(filtering, ordering, limit, offset);
    return {
      type: LOOKING_FOR_LIST,
      payload: request.get(`${dictUrl}job_types/`, params)
    };
}

export function locationList(filtering, ordering, limit, offset) {
    let params = prepareParams(filtering, ordering, limit, offset);
    return {
      type: LOCATION_LIST,
      payload: request.get(`${commonUrl}locations/`, params)
    };
}

export function industryList(filtering, ordering, limit, offset) {
    let params = prepareParams(filtering, ordering, limit, offset);
    return {
      type: INDUSTRY_LIST,
      payload: request.get(`${dictUrl}industries/`, params)
    };
}

export function roleList(filtering, ordering, limit, offset) {
    let params = prepareParams(filtering, ordering, limit, offset);
    return {
      type: ROLE_LIST,
      payload: request.get(`${dictUrl}roles/`, params)
    };
}

export function countryList(filtering, ordering, limit, offset) {
    let params = prepareParams(filtering, ordering, limit, offset);
    return {
      type: COUNTRY_LIST,
      payload: request.get(`${dictUrl}countries/`, params)
    };
}
export function stateList(filtering, ordering, limit, offset) {
    let params = prepareParams(filtering, ordering, limit, offset);
    return {
      type: STATE_LIST,
      payload: request.get(`${dictUrl}states/`, params)
    };
}
export function cityList(filtering, ordering, limit, offset) {
    let params = prepareParams(filtering, ordering, limit, offset);
    return {
      type: CITY_LIST,
      payload: request.get(`${dictUrl}cities/`, params)
    };
}
