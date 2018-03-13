import {
    JOB_PROFILE_LIST,
    JOB_PROFILE_CREATE,
    JOB_PROFILE_UPDATE,
    JOB_PROFILE_MARK_DEFAULT,
    JOB_PROFILE_DELETE,
    JOB_PROFILE_SHOW_EDIT_MODAL,
    JOB_PROFILE_HIDE_EDIT_MODAL,
    JOB_PROFILE_SELECT
} from '../constants';


const initialState = {
    jobProfiles: [],
    jobProfile: {},
    selectedJobProfile: {},
    loading: false,
    isShownJobProfileEditModal: false,
    errors: [],
};

export default function jobProfileReducer(state = initialState, action) {
    switch (action.type) {
        ////////////////////////////////////////////////////////
        //                  JOB_PROFILE_LIST                  //
        ////////////////////////////////////////////////////////
        case JOB_PROFILE_LIST + '_FULFILLED': {
            let selectedJobProfile = action.payload.data.results.filter(item => item.is_default === true);
            return Object.assign({}, state, {
                jobProfiles: action.payload.data.results,
                selectedJobProfile: selectedJobProfile.length > 0 ? selectedJobProfile[0] : {},
                loading: false,
                isShownJobProfileEditModal: false,
                errors: {}
            });
        }

        case JOB_PROFILE_LIST + '_PENDING': {
          return {
            ...state,
            loading: true,
            isShownJobProfileEditModal: false,
            errors: {}
          }
        }

        case JOB_PROFILE_LIST + '_REJECTED': {
          return {
            ...state,
            loading: false,
            isShownJobProfileEditModal: false,
            errors: { global: action.payload.message }
          }
        }

        ////////////////////////////////////////////////////////
        //                  JOB_PROFILE_CREATE                //
        ////////////////////////////////////////////////////////
        case JOB_PROFILE_CREATE + '_FULFILLED': {
            return {
                ...state,
                jobProfiles: [...state.jobProfiles, action.payload.data],
                errors: {}
            };
        }

        case JOB_PROFILE_CREATE + '_PENDING': {
          return {
            ...state,
            errors: {}
          }
        }

        case JOB_PROFILE_CREATE + '_REJECTED': {
          return {
            ...state,
            errors: { global: action.payload.message }
          }
        }

        ////////////////////////////////////////////////////////
        //                  JOB_PROFILE_UPDATE                //
        ////////////////////////////////////////////////////////
        case JOB_PROFILE_UPDATE + '_FULFILLED': {
            return {
                ...state,
                jobProfiles: state.jobProfiles.map(
                    jobProfile => jobProfile.id === action.payload.data.id ?
                    action.payload.data :
                    jobProfile
                ),
                errors: {}
            };
        }

        case JOB_PROFILE_UPDATE + '_PENDING': {
          return {
            ...state,
            errors: {}
          }
        }

        case JOB_PROFILE_UPDATE + '_REJECTED': {
          return {
            ...state,
            errors: { global: action.payload.message }
          }
        }

        ////////////////////////////////////////////////////////
        //               JOB_PROFILE_MARK_DEFAULT             //
        ////////////////////////////////////////////////////////
        case JOB_PROFILE_MARK_DEFAULT + '_FULFILLED': {
            return {
                ...state,
                jobProfiles: state.jobProfiles.map(function (jobProfile) {
                    if (jobProfile.id === action.payload.data.id) {
                        return action.payload.data
                    }
                    let updatedJobProfile = Object.assign({}, jobProfile);
                    updatedJobProfile.is_default = false;
                    return updatedJobProfile
                }),
                errors: {}
            };
        }

        case JOB_PROFILE_MARK_DEFAULT + '_PENDING': {
          return {
            ...state,
            errors: {}
          }
        }

        case JOB_PROFILE_MARK_DEFAULT + '_REJECTED': {
          return {
            ...state,
            errors: { global: action.payload.message }
          }
        }

        ////////////////////////////////////////////////////////
        //                  JOB_PROFILE_DELETE                //
        ////////////////////////////////////////////////////////

        case JOB_PROFILE_DELETE + '_FULFILLED': {
          const id = action.payload.config.id;
          return {
            ...state,
            jobProfiles: state.jobProfiles.filter(item => item.id !== id),
            errors: {}
          }
        }

        case JOB_PROFILE_DELETE + '_PENDING': {
          return {
            ...state,
            errors: {}
          }
        }

        case JOB_PROFILE_DELETE + '_REJECTED': {
          return {
            ...state,
            errors: { global: action.payload.message }
          }
        }

        ////////////////////////////////////////////////////////
        //               JOB_PROFILE_EDIT_MODAL               //
        ////////////////////////////////////////////////////////

        case JOB_PROFILE_SHOW_EDIT_MODAL: {
          return {
            ...state,
            isShownJobProfileEditModal: true,
            jobProfile: action.jobProfile,
            errors: {}
          }
        }

        case JOB_PROFILE_HIDE_EDIT_MODAL: {
          return {
            ...state,
            isShownJobProfileEditModal: false,
            jobProfile: {},
            errors: {}
          }

        }

        case JOB_PROFILE_SELECT: {
          return {
            ...state,
            selectedJobProfile: action.profile,
            errors: {}
          }
        }

        default:
            return state;
    }
}
