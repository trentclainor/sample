import {
    EDUCATION_LIST,
    EDUCATION_CREATE,
    EDUCATION_UPDATE,
    EDUCATION_DELETE,
    EDUCATION_SHOW_EDIT_MODAL,
    EDUCATION_HIDE_EDIT_MODAL
} from '../constants';

const initialState = {
    educations: [],
    education: {},
    loading: false,
    isShownEducationEditModal: false,
    errors: [],
};

export default function profileEducationReducer(state = initialState, action) {
    switch (action.type) {
        ////////////////////////////////////////////////////////
        //                   EDUCATION_LIST                   //
        ////////////////////////////////////////////////////////
        case EDUCATION_LIST + '_FULFILLED': {
            return Object.assign({}, state, {
                educations: action.payload.data.results,
                loading: false,
                isShownEducationEditModal: false,
                errors: {}
            });
        }

        case EDUCATION_LIST + '_PENDING': {
          return {
            ...state,
            loading: true,
            isShownEducationEditModal: false,
            errors: {}
          }
        }

        case EDUCATION_LIST + '_REJECTED': {
          return {
            ...state,
            loading: false,
            isShownEducationEditModal: false,
            errors: { global: action.payload.message }
          }
        }

        ////////////////////////////////////////////////////////
        //                  EDUCATION_CREATE                  //
        ////////////////////////////////////////////////////////
        case EDUCATION_CREATE + '_FULFILLED': {
            return {
                ...state,
                educations: [...state.educations, action.payload.data],
                errors: {}
            };
        }

        case EDUCATION_CREATE + '_PENDING': {
          return {
            ...state,
            errors: {}
          }
        }

        case EDUCATION_CREATE + '_REJECTED': {
          return {
            ...state,
            errors: { global: action.payload.message }
          }
        }

        ////////////////////////////////////////////////////////
        //                   EDUCATION_UPDATE                 //
        ////////////////////////////////////////////////////////
        case EDUCATION_UPDATE + '_FULFILLED': {
            return {
                ...state,
                educations: state.educations.map(
                    education => education.id === action.payload.data.id ?
                    action.payload.data :
                    education
                ),
                errors: {}
            };
        }

        case EDUCATION_UPDATE + '_PENDING': {
          return {
            ...state,
            errors: {}
          }
        }

        case EDUCATION_UPDATE + '_REJECTED': {
          return {
            ...state,
            errors: { global: action.payload.message }
          }
        }

        ////////////////////////////////////////////////////////
        //                   EDUCATION_DELETE                 //
        ////////////////////////////////////////////////////////

        case EDUCATION_DELETE + '_FULFILLED': {
          const id = action.payload.config.id;
          return {
            ...state,
            educations: state.educations.filter(item => item.id !== id),
            errors: {}
          }
        }

        case EDUCATION_DELETE + '_PENDING': {
          return {
            ...state,
            errors: {}
          }
        }

        case EDUCATION_DELETE + '_REJECTED': {
          return {
            ...state,
            errors: { global: action.payload.message }
          }
        }

        ////////////////////////////////////////////////////////
        //                EDUCATION_EDIT_MODAL                //
        ////////////////////////////////////////////////////////

        case EDUCATION_SHOW_EDIT_MODAL: {
          return {
            ...state,
            isShownEducationEditModal: true,
            education: action.education,
            errors: {}
          }
        }

        case EDUCATION_HIDE_EDIT_MODAL: {
          return {
            ...state,
            isShownEducationEditModal: false,
            education: {},
            errors: {}
          }
        }

        default:
            return state;
    }
}
