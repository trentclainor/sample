import {
    VACANCY_LIST,
    VACANCY_CREATE,
    VACANCY_UPDATE,
    VACANCY_DELETE,
    APPLY_SEARCH_FILTERS,
    VACANCY_STANDARD_SEARCH,
    VACANCY_PERSONALIZED_SEARCH
} from '../constants';
import {COUNT_PER_PAGE} from "../utils/config";


const initialState = {
    itemsCount: null,
    nextLink: null,
    previousLink: null,
    items: [],
    item: {},
    searchParams: {},
    filters: {
        search_type: "Standard",
        limit: COUNT_PER_PAGE,
        offset: 0,
        ordering: '-modified'
    },
    loading: false,
    errors: [],
};

export default function vacancyReducer(state = initialState, action) {
    switch (action.type) {
        ////////////////////////////////////////////////////////
        //                    VACANCY_LIST                    //
        ////////////////////////////////////////////////////////
        case VACANCY_LIST + '_FULFILLED': {
            return Object.assign({}, state, {
                items: action.payload.data.results,
                itemsCount: action.payload.data.count,
                nextLink: action.payload.data.next,
                previousLink: action.payload.data.previous,
                loading: false,
                errors: {}
            });
        }

        case VACANCY_LIST + '_PENDING': {
            return {
                ...state,
                loading: true,
                errors: {}
            }
        }

        case VACANCY_LIST + '_REJECTED': {
            return {
                ...state,
                loading: false,
                errors: { global: action.payload.message }
            }
        }

        ////////////////////////////////////////////////////////
        //                    VACANCY_CREATE                  //
        ////////////////////////////////////////////////////////
        case VACANCY_CREATE + '_FULFILLED': {
            return {
                ...state,
                items: [...state.items, action.payload.data],
                itemsCount: state.itemsCount + 1,
                errors: {}
            };
        }

        case VACANCY_CREATE + '_PENDING': {
            return {
                ...state,
                errors: {}
            }
        }

        case VACANCY_CREATE + '_REJECTED': {
            return {
                ...state,
                errors: { global: action.payload.message }
            }
        }

        ////////////////////////////////////////////////////////
        //                    VACANCY_UPDATE                  //
        ////////////////////////////////////////////////////////
        case VACANCY_UPDATE + '_FULFILLED': {
            return {
                ...state,
                items: state.items.map(
                    item => item.id === action.payload.data.id ?
                        action.payload.data :
                        item
                ),
                errors: {}
            };
        }

        case VACANCY_UPDATE + '_PENDING': {
            return {
                ...state,
                errors: {}
            }
        }

        case VACANCY_UPDATE + '_REJECTED': {
            return {
                ...state,
                errors: { global: action.payload.message }
            }
        }

        ////////////////////////////////////////////////////////
        //                    VACANCY_DELETE                  //
        ////////////////////////////////////////////////////////

        case VACANCY_DELETE + '_FULFILLED': {
            const id = action.payload.config.id;
            return {
                ...state,
                items: state.items.filter(item => item.id !== id),
                itemsCount: state.itemsCount - 1,
                errors: {}
            }
        }

        case VACANCY_DELETE + '_PENDING': {
            return {
                ...state,
                errors: {}
            }
        }

        case VACANCY_DELETE + '_REJECTED': {
            return {
                ...state,
                errors: { global: action.payload.message }
            }
        }

        ////////////////////////////////////////////////////////
        //              VACANCY_STANDARD_SEARCH               //
        ////////////////////////////////////////////////////////
        case VACANCY_STANDARD_SEARCH + '_FULFILLED': {
            return Object.assign({}, state, {
                items: action.payload.data.results,
                itemsCount: action.payload.data.count,
                nextLink: action.payload.data.next,
                previousLink: action.payload.data.previous,
                loading: false,
                errors: {}
            });
        }

        case VACANCY_STANDARD_SEARCH + '_PENDING': {
            return {
                ...state,
                loading: true,
                errors: {}
            }
        }

        case VACANCY_STANDARD_SEARCH + '_REJECTED': {
            return {
                ...state,
                loading: false,
                errors: { global: action.payload.message }
            }
        }

        ////////////////////////////////////////////////////////
        //            VACANCY_PERSONALIZED_SEARCH             //
        ////////////////////////////////////////////////////////
        case VACANCY_PERSONALIZED_SEARCH + '_FULFILLED': {
            return Object.assign({}, state, {
                items: action.payload.data.results,
                itemsCount: action.payload.data.count,
                nextLink: action.payload.data.next,
                previousLink: action.payload.data.previous,
                loading: false,
                errors: {}
            });
        }

        case VACANCY_PERSONALIZED_SEARCH + '_PENDING': {
            return {
                ...state,
                loading: true,
                errors: {}
            }
        }

        case VACANCY_PERSONALIZED_SEARCH + '_REJECTED': {
            return {
                ...state,
                loading: false,
                errors: { global: action.payload.message }
            }
        }

        ////////////////////////////////////////////////////////
        //                APPLY_SEARCH_FILTERS                //
        ////////////////////////////////////////////////////////
        case APPLY_SEARCH_FILTERS: {
            let filters = Object.assign({}, state.filters, action.payload);

            return Object.assign({}, state, {
                filters: filters,
            });
        }

        default:
            return state;
    }
}
