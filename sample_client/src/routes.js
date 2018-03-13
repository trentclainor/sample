import React from 'react';
import { Route, Switch } from 'react-router';

import requireAuthentication from './utils/requireAuthentication';

import AboutView from "./views/about/About";
import HomeView from "./views/home/Home";
import NotFoundView from "./views/notFound/NotFound";
import ProfileView from "./views/profile/Profile";
import LoginView from "./views/login/Login";
import SearchView from "./views/jobSearch/SearchForm";
import SearchResultsView from "./views/jobSearch/SearchResults";

export default(
   <Switch>
       <Route exact path='/' component={HomeView}/>
       <Route path='/about' component={AboutView}/>
       <Route path='/login' component={LoginView}/>
       <Route path='/users/:userId/profile' component={requireAuthentication(ProfileView)} />
       <Route path='/profile' component={requireAuthentication(ProfileView)} />
       <Route path='/search/results' component={requireAuthentication(SearchResultsView)} />
       <Route path='/search' component={requireAuthentication(SearchView)} />
       <Route path='*' component={NotFoundView} />
   </Switch>
);
