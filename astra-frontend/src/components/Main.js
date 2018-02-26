import React from 'react';
import TopBar from './TopBar';
import { Switch, Route, Redirect} from 'react-router-dom';
import CurrentUserStore from '../stores/CurrentUserStore'

import DashboardView from "./DashboardView"
import LoginView from "./LoginView"

require('core-js/es6');
require('core-js/es7');

class Main extends React.Component {
  constructor(props) {
    super(props);
    this.state = {loggedIn: (CurrentUserStore.getCurrentUser() != null)};
  }

  render() {
    return (
      <main>
        <TopBar />
        <Switch>
          <Route path="/login" render={() => this.state.loggedIn ?
            <Redirect to="/dashboard"/> : <LoginView/> }/>
          <Route path="/dashboard" component={DashboardView}/>
          {/*
          <Route path="/login/forgot-password" component={ForgotPasswordView}/>
          <Route path="/devices" component={DevicesView}/>
          <Route path="/devices/:id" component={DevicesDetailView}/>
          <Route path="/projects" component={ProjectView}/>
          <Route path="/projects/:id" component={ProjectDetailView}/>
          <Route path="/balance" component={BalanceView}/>
          <Route path="/balance/add-tokens" component={BalanceAddView}/>
          <Route path="/account" component={AccountView}/> 
          <Route path="*" component={NotFoundView}/>
        */}
        </Switch>
      </main>
    );
  }
}

export default Main;