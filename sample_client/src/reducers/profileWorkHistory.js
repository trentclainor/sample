import {
    WORK_HISTORY_LIST,
    WORK_HISTORY_CREATE,
    WORK_HISTORY_UPDATE,
    WORK_HISTORY_DELETE,
    WORK_HISTORY_SHOW_EDIT_MODAL,
    WORK_HISTORY_HIDE_EDIT_MODAL
} from '../constants';

const initialState = {
    workHistories: [],
    workHistory: {},
    loading: false,
    isShownWorkHistoryEditModal: false,
    errors: [],
};

export default function profileWorkHistoryReducer(state = initialState, action) {
    switch (action.type) {
        ////////////////////////////////////////////////////////
        //                  WORK_HISTORY_LIST                 //
        ////////////////////////////////////////////////////////
        case WORK_HISTORY_LIST + '_FULFILLED': {
            return Object.assign({}, state, {
                workHistories: action.payload.data.results,
                loading: false,
                isShownWorkHistoryEditModal: false,
                errors: {}
            });
        }

        case WORK_HISTORY_LIST + '_PENDING': {
          return {
            ...state,
            loading: true,
            isShownWorkHistoryEditModal: false,
            errors: {}
          }
        }

        case WORK_HISTORY_LIST + '_REJECTED': {
          return {
            ...state,
            loading: false,
            isShownWorkHistoryEditModal: false,
            errors: { global: action.payload.message }
          }
        }

        ////////////////////////////////////////////////////////
        //                  WORK_HISTORY_CREATE               //
        ////////////////////////////////////////////////////////
        case WORK_HISTORY_CREATE + '_FULFILLED': {
            return {
                ...state,
                workHistories: [...state.workHistories, action.payload.data],
                errors: {}
            };
        }

        case WORK_HISTORY_CREATE + '_PENDING': {
          return {
            ...state,
            errors: {}
          }
        }

        case WORK_HISTORY_CREATE + '_REJECTED': {
          return {
            ...state,
            errors: { global: action.payload.message }
          }
        }

        ////////////////////////////////////////////////////////
        //                  WORK_HISTORY_UPDATE               //
        ////////////////////////////////////////////////////////
        case WORK_HISTORY_UPDATE + '_FULFILLED': {
            return {
                ...state,
                workHistories: state.workHistories.map(
                    workHistory => workHistory.id === action.payload.data.id ?
                    action.payload.data :
                    workHistory
                ),
                errors: {}
            };
        }

        case WORK_HISTORY_UPDATE + '_PENDING': {
          return {
            ...state,
            errors: {}
          }
        }

        case WORK_HISTORY_UPDATE + '_REJECTED': {
          return {
            ...state,
            errors: { global: action.payload.message }
          }
        }

        ////////////////////////////////////////////////////////
        //                  WORK_HISTORY_DELETE               //
        ////////////////////////////////////////////////////////

        case WORK_HISTORY_DELETE + '_FULFILLED': {
          const id = action.payload.config.id;
          return {
            ...state,
            workHistories: state.workHistories.filter(item => item.id !== id),
            errors: {}
          }
        }

        case WORK_HISTORY_DELETE + '_PENDING': {
          return {
            ...state,
            errors: {}
          }
        }

        case WORK_HISTORY_DELETE + '_REJECTED': {
          return {
            ...state,
            errors: { global: action.payload.message }
          }
        }

        ////////////////////////////////////////////////////////
        //                BASIC_INFO_EDIT_MODAL               //
        ////////////////////////////////////////////////////////

        case WORK_HISTORY_SHOW_EDIT_MODAL: {
          return {
            ...state,
            isShownWorkHistoryEditModal: true,
            workHistory: action.workHistory,
            errors: {}
          }
        }

        case WORK_HISTORY_HIDE_EDIT_MODAL: {
          return {
            ...state,
            isShownWorkHistoryEditModal: false,
            workHistory: {},
            errors: {}
          }
        }

        default:
            return state;
    }
}
