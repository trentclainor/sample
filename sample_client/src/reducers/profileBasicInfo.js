import {
    BASIC_INFO_LIST,
    BASIC_INFO_CREATE,
    BASIC_INFO_UPDATE,
    BASIC_INFO_SHOW_EDIT_MODAL,
    BASIC_INFO_HIDE_EDIT_MODAL
} from '../constants';

const initialState = {
    basicInfos: [],
    basicInfo: {},
    loading: false,
    isShownBasicInfoEditModal: false,
    errors: [],
};

export default function profileBasicInfoReducer(state = initialState, action) {
    switch (action.type) {
        ////////////////////////////////////////////////////////
        //                  BASIC_INFO_LIST                   //
        ////////////////////////////////////////////////////////
        case BASIC_INFO_LIST + '_FULFILLED': {
            return Object.assign({}, state, {
                basicInfos: action.payload.data.results,
                loading: false,
                isShownBasicInfoEditModal: false,
                errors: {}
            });
        }

        case BASIC_INFO_LIST + '_PENDING': {
          return {
            ...state,
            loading: true,
            isShownBasicInfoEditModal: false,
            errors: {}
          }
        }

        case BASIC_INFO_LIST + '_REJECTED': {
          return {
            ...state,
            loading: false,
            isShownBasicInfoEditModal: false,
            errors: { global: action.payload.message }
          }
        }

        ////////////////////////////////////////////////////////
        //                  BASIC_INFO_CREATE                 //
        ////////////////////////////////////////////////////////
        case BASIC_INFO_CREATE + '_FULFILLED': {
            return {
                ...state,
                basicInfos: [...state.basicInfos, action.payload.data],
                errors: {}
            };
        }

        case BASIC_INFO_CREATE + '_PENDING': {
          return {
            ...state,
            errors: {}
          }
        }

        case BASIC_INFO_CREATE + '_REJECTED': {
          return {
            ...state,
            errors: { global: action.payload.message }
          }
        }

        ////////////////////////////////////////////////////////
        //                  BASIC_INFO_UPDATE                 //
        ////////////////////////////////////////////////////////
        case BASIC_INFO_UPDATE + '_FULFILLED': {
            return {
                ...state,
                basicInfos: state.basicInfos.map(
                    basicInfo => basicInfo.id === action.payload.data.id ?
                    action.payload.data :
                    basicInfo
                ),
                errors: {}
            };
        }

        case BASIC_INFO_UPDATE + '_PENDING': {
          return {
            ...state,
            errors: {}
          }
        }

        case BASIC_INFO_UPDATE + '_REJECTED': {
          return {
            ...state,
            errors: { global: action.payload.message }
          }
        }

        ////////////////////////////////////////////////////////
        //                BASIC_INFO_EDIT_MODAL               //
        ////////////////////////////////////////////////////////

        case BASIC_INFO_SHOW_EDIT_MODAL: {
          return {
            ...state,
            isShownBasicInfoEditModal: true,
            errors: {}
          }
        }

        case BASIC_INFO_HIDE_EDIT_MODAL: {
          return {
            ...state,
            isShownBasicInfoEditModal: false,
            errors: {}
          }
        }

        default:
            return state;
    }
}
