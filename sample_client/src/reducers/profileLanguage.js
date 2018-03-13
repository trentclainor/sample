import {
    LANGUAGE_LIST,
    LANGUAGE_CREATE,
    LANGUAGE_UPDATE,
    LANGUAGE_DELETE,
    LANGUAGE_SHOW_EDIT_MODAL,
    LANGUAGE_HIDE_EDIT_MODAL
} from '../constants';

const initialState = {
    languages: [],
    language: {},
    loading: false,
    isShownLanguageEditModal: false,
    errors: [],
};

export default function profileLanguageReducer(state = initialState, action) {
    switch (action.type) {
        ////////////////////////////////////////////////////////
        //                   LANGUAGE_LIST                   //
        ////////////////////////////////////////////////////////
        case LANGUAGE_LIST + '_FULFILLED': {
            return Object.assign({}, state, {
                languages: action.payload.data.results,
                loading: false,
                isShownLanguageEditModal: false,
                errors: {}
            });
        }

        case LANGUAGE_LIST + '_PENDING': {
          return {
            ...state,
            loading: true,
            isShownLanguageEditModal: false,
            errors: {}
          }
        }

        case LANGUAGE_LIST + '_REJECTED': {
          return {
            ...state,
            loading: false,
            isShownLanguageEditModal: false,
            errors: { global: action.payload.message }
          }
        }

        ////////////////////////////////////////////////////////
        //                  LANGUAGE_CREATE                  //
        ////////////////////////////////////////////////////////
        case LANGUAGE_CREATE + '_FULFILLED': {
            return {
                ...state,
                languages: [...state.languages, action.payload.data],
                errors: {}
            };
        }

        case LANGUAGE_CREATE + '_PENDING': {
          return {
            ...state,
            errors: {}
          }
        }

        case LANGUAGE_CREATE + '_REJECTED': {
          return {
            ...state,
            errors: { global: action.payload.message }
          }
        }

        ////////////////////////////////////////////////////////
        //                   LANGUAGE_UPDATE                 //
        ////////////////////////////////////////////////////////
        case LANGUAGE_UPDATE + '_FULFILLED': {
            return {
                ...state,
                languages: state.languages.map(
                    language => language.id === action.payload.data.id ?
                    action.payload.data :
                    language
                ),
                errors: {}
            };
        }

        case LANGUAGE_UPDATE + '_PENDING': {
          return {
            ...state,
            errors: {}
          }
        }

        case LANGUAGE_UPDATE + '_REJECTED': {
          return {
            ...state,
            errors: { global: action.payload.message }
          }
        }

        ////////////////////////////////////////////////////////
        //                   LANGUAGE_DELETE                 //
        ////////////////////////////////////////////////////////

        case LANGUAGE_DELETE + '_FULFILLED': {
          const id = action.payload.config.id;
          return {
            ...state,
            languages: state.languages.filter(item => item.id !== id),
            errors: {}
          }
        }

        case LANGUAGE_DELETE + '_PENDING': {
          return {
            ...state,
            errors: {}
          }
        }

        case LANGUAGE_DELETE + '_REJECTED': {
          return {
            ...state,
            errors: { global: action.payload.message }
          }
        }

        ////////////////////////////////////////////////////////
        //                LANGUAGE_EDIT_MODAL                //
        ////////////////////////////////////////////////////////

        case LANGUAGE_SHOW_EDIT_MODAL: {
          return {
            ...state,
            isShownLanguageEditModal: true,
            language: action.language,
            errors: {}
          }
        }

        case LANGUAGE_HIDE_EDIT_MODAL: {
          return {
            ...state,
            isShownLanguageEditModal: false,
            language: {},
            errors: {}
          }
        }

        default:
            return state;
    }
}
