import { combineReducers } from 'redux';
import { routerReducer } from 'react-router-redux';
import { reducer as formReducer } from 'redux-form'
import authReducer from './auth';
import jobProfileReducer from './jobProfile';
import profileBasicInfoReducer from './profileBasicInfo';
import profileWorkHistoryReducer from './profileWorkHistory';
import profileEducationReducer from './profileEducation';
import profileLanguageReducer from './profileLanguage';
import profileSearchPreferenceReducer from './profileSearchPreference';
import vacancyReducer from './vacancy'
import dictHelpersReducer from './dictHelpers';

export default combineReducers({
    auth: authReducer,
    jobProfile: jobProfileReducer,
    profileBasicInfo: profileBasicInfoReducer,
    profileWorkHistory: profileWorkHistoryReducer,
    profileEducation: profileEducationReducer,
    profileLanguage: profileLanguageReducer,
    profilePreference: profileSearchPreferenceReducer,
    vacancy: vacancyReducer,
    dictHelpers: dictHelpersReducer,
    form: formReducer,
    routing: routerReducer
});
