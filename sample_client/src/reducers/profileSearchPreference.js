import {
    SEARCH_PREFERENCE_LIST,
    SEARCH_PREFERENCE_CREATE,
    SEARCH_PREFERENCE_UPDATE,
} from '../constants';

const initialState = {
    preferences: [],
    preference: {},
    loading: false,
    errors: [],
};

export default function profileSearchPreferenceReducer(state = initialState, action) {
    switch (action.type) {
        ////////////////////////////////////////////////////////
        //               SEARCH_PREFERENCE_LIST               //
        ////////////////////////////////////////////////////////
        case SEARCH_PREFERENCE_LIST + '_FULFILLED': {
            return Object.assign({}, state, {
                preferences: action.payload.data.results,
                loading: false,
                errors: {}
            });
        }

        case SEARCH_PREFERENCE_LIST + '_PENDING': {
          return {
            ...state,
            loading: true,
            errors: {}
          }
        }

        case SEARCH_PREFERENCE_LIST + '_REJECTED': {
          return {
            ...state,
            loading: false,
            errors: { global: action.payload.message }
          }
        }

        ////////////////////////////////////////////////////////
        //              SEARCH_PREFERENCE_CREATE              //
        ////////////////////////////////////////////////////////
        case SEARCH_PREFERENCE_CREATE + '_FULFILLED': {
            return {
                ...state,
                preferences: [...state.preferences, action.payload.data],
                errors: {}
            };
        }

        case SEARCH_PREFERENCE_CREATE + '_PENDING': {
          return {
            ...state,
            errors: {}
          }
        }

        case SEARCH_PREFERENCE_CREATE + '_REJECTED': {
          return {
            ...state,
            errors: { global: action.payload.message }
          }
        }

        ////////////////////////////////////////////////////////
        //               SEARCH_PREFERENCE_UPDATE             //
        ////////////////////////////////////////////////////////
        case SEARCH_PREFERENCE_UPDATE + '_FULFILLED': {
            return {
                ...state,
                preferences: state.preferences.map(
                    preference => preference.id === action.payload.data.id ?
                    action.payload.data :
                    preference
                ),
                errors: {}
            };
        }

        case SEARCH_PREFERENCE_UPDATE + '_PENDING': {
          return {
            ...state,
            errors: {}
          }
        }

        case SEARCH_PREFERENCE_UPDATE + '_REJECTED': {
          return {
            ...state,
            errors: { global: action.payload.message }
          }
        }

        default:
            return state;
    }
}
