'use strict';

import React from 'react';
import ReactDOM from 'react-dom';

require('core-js/es6');
require('core-js/es7');

var IndexRoute = ReactRouter.IndexRoute;
var Router = ReactRouter.Router;
var Route = ReactRouter.Route;

var routes = (
  <Route path="/" component={AstraWeb}>
    <Route path="/login" component={LoginView}/>
    <Route path="/login/forgot-password" component={ForgotPasswordView}/>
    <Route path="/dashboard" component={DashboardView}/>
    <Route path="/devices" component={DevicesView}/>
    <Route path="/devices/:id" component={DevicesDetailView}/>
    <Route path="/projects" component={ProjectView}/>
    <Route path="/projects/:id" component={ProjectDetailView}/>
    <Route path="/balance" component={BalanceView}/>
    <Route path="/balance/add-tokens" component={BalanceAddView}/>
    <Route path="/account" component={AccountView}/> 
    <IndexRoute component={RedirectView} />
    <Route path="*" component={NotFoundView}/>
  </Route>
)

window.addEventListener('DOMContentLoaded', () => {
  ReactDOM.render(
    <Router>
      {routes}
    </Router>,
    document.getElementById('astra-app'),
  );
});
