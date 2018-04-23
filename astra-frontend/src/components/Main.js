import React from 'react';
import { Switch, Route, Redirect} from 'react-router-dom';
import CurrentUserStore from '../stores/CurrentUserStore'

import InitialView from './InitialView'
import Dashboard from './core/Dashboard'

require('core-js/es6');
require('core-js/es7');

class Main extends React.Component {
  constructor(props) {
    super(props);
    this.state = {loggedIn: (CurrentUserStore.getUserEmail() != null)};
  }

  render() {
    return (
      <main>
        <Switch>
          <Route path="/login" render={() => this.state.loggedIn ?
            <Redirect to="/devices"/> : <InitialView/> }/>
          <Route path="/welcome" render={() => <Dashboard type='welcome'/>}/>
          <Route path="/devices" render={() => <Dashboard type='devices'/>}/>
        </Switch>
      </main>
    );
  }
}

export default Main;