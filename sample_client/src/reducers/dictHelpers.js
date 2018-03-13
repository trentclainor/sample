import {
    LOOKING_FOR_LIST,
    LOCATION_LIST,
    INDUSTRY_LIST,
    ROLE_LIST,
    COUNTRY_LIST,
    STATE_LIST,
    CITY_LIST
} from '../constants';


const initialState = {
    lookingForList: [],
    lookingForListLoading: false,
    lookingForListErrors: [],

    locationList: [],
    locationListLoading: false,
    locationListErrors: [],

    industryList: [],
    industryListLoading: false,
    industryListErrors: [],

    roleList: [],
    roleListLoading: false,
    roleListErrors: [],

    countryList: [],
    countryListLoading: false,
    countryListErrors: [],

    stateList: [],
    stateListLoading: false,
    stateListErrors: [],

    cityList: [],
    cityListLoading: false,
    cityListErrors: [],
};

export default function dictHelpersReducer(state = initialState, action) {
    switch (action.type) {
        ////////////////////////////////////////////////////////
        //                  LOOKING_FOR_LIST                  //
        ////////////////////////////////////////////////////////
        case LOOKING_FOR_LIST + '_FULFILLED': {
            return Object.assign({}, state, {
                lookingForList: action.payload.data,
                lookingForListLoading: false,
                lookingForListErrors: {}
            });
        }

        case LOOKING_FOR_LIST + '_PENDING': {
          return {
            ...state,
            lookingForListLoading: true,
            lookingForListErrors: {}
          }
        }

        case LOOKING_FOR_LIST + '_REJECTED': {
          return {
            ...state,
            lookingForListLoading: false,
            lookingForListErrors: { global: action.payload.message }
          }
        }

        ////////////////////////////////////////////////////////
        //                    LOCATION_LIST                   //
        ////////////////////////////////////////////////////////
        case LOCATION_LIST + '_FULFILLED': {
            return Object.assign({}, state, {
                locationList: action.payload.data.results,
                locationListLoading: false,
                locationListErrors: {}
            });
        }

        case LOCATION_LIST + '_PENDING': {
          return {
            ...state,
            locationListLoading: true,
            locationListErrors: {}
          }
        }

        case LOCATION_LIST + '_REJECTED': {
          return {
            ...state,
            locationListLoading: false,
            locationListErrors: { global: action.payload.message }
          }
        }

        ////////////////////////////////////////////////////////
        //                   INDUSTRY_LIST                    //
        ////////////////////////////////////////////////////////
        case INDUSTRY_LIST + '_FULFILLED': {
            return Object.assign({}, state, {
                industryList: action.payload.data,
                industryListLoading: false,
                industryListErrors: {}
            });
        }

        case INDUSTRY_LIST + '_PENDING': {
          return {
            ...state,
            industryListLoading: true,
            industryListErrors: {}
          }
        }

        case INDUSTRY_LIST + '_REJECTED': {
          return {
            ...state,
            industryListLoading: false,
            industryListErrors: { global: action.payload.message }
          }
        }

        ////////////////////////////////////////////////////////
        //                      ROLE_LIST                     //
        ////////////////////////////////////////////////////////
        case ROLE_LIST + '_FULFILLED': {
            return Object.assign({}, state, {
                roleList: action.payload.data,
                roleListLoading: false,
                roleListErrors: {}
            });
        }

        case ROLE_LIST + '_PENDING': {
          return {
            ...state,
            roleListLoading: true,
            roleListErrors: {}
          }
        }

        case ROLE_LIST + '_REJECTED': {
          return {
            ...state,
            roleListLoading: false,
            roleListErrors: { global: action.payload.message }
          }
        }

        ////////////////////////////////////////////////////////
        //                   COUNTRY_LIST                     //
        ////////////////////////////////////////////////////////
        case COUNTRY_LIST + '_FULFILLED': {
            return Object.assign({}, state, {
                countryList: action.payload.data,
                countryListLoading: false,
                countryListErrors: {}
            });
        }

        case COUNTRY_LIST + '_PENDING': {
          return {
            ...state,
            countryListLoading: true,
            countryListErrors: {}
          }
        }

        case COUNTRY_LIST + '_REJECTED': {
          return {
            ...state,
            countryListLoading: false,
            countryListErrors: { global: action.payload.message }
          }
        }

        ////////////////////////////////////////////////////////
        //                     STATE_LIST                     //
        ////////////////////////////////////////////////////////
        case STATE_LIST + '_FULFILLED': {
            return Object.assign({}, state, {
                stateList: action.payload.data,
                stateListLoading: false,
                stateListErrors: {}
            });
        }

        case STATE_LIST + '_PENDING': {
          return {
            ...state,
            stateListLoading: true,
            stateListErrors: {}
          }
        }

        case STATE_LIST + '_REJECTED': {
          return {
            ...state,
            stateListLoading: false,
            stateListErrors: { global: action.payload.message }
          }
        }

        ////////////////////////////////////////////////////////
        //                      CITY_LIST                     //
        ////////////////////////////////////////////////////////
        case CITY_LIST + '_FULFILLED': {
            return Object.assign({}, state, {
                cityList: action.payload.data,
                cityListLoading: false,
                cityListErrors: {}
            });
        }

        case CITY_LIST + '_PENDING': {
          return {
            ...state,
            cityListLoading: true,
            cityListErrors: {}
          }
        }

        case CITY_LIST + '_REJECTED': {
          return {
            ...state,
            cityListLoading: false,
            cityListErrors: { global: action.payload.message }
          }
        }


        default:
            return state;
    }
}
