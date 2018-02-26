import ActionConstants from '../constants/ActionConstants'
import Dispatcher from '../dispatcher'
import ServerAPI from '../ServerAPI'
import {Store} from 'flux/utils'
import image from '../images/Phone.png'


class CurrentUserStore extends Store {
  constructor(dispatcher) {
    super(dispatcher);
    this._currentUser = null;
    this.state = {
      _userData: {
        first_name: 'Soham',
        last_name: 'Kale',
        selfie: null,
      },
      _userBalance: {
        starBalance: 35,
        earningRate: 23,
      },
      _userErrors: {},
    };
  }

  getCurrentUser() { 
    return this.state._currentUser;
  }

  getUserPanelData() {
    return {
      name: this.state._userData.first_name + this.state._userData.last_name, 
      image: this.state._userData.selfie,
      starBalance: this.state._userBalance.star_balance,
      earningRate: this.state._userBalance.earning_rate,
    };
  }

  __onDispatch(action) {
    switch(action.actionType) {
      case ActionConstants.LOGIN:
        if (action.status == "401") {
          this.setState({_userErrors: {
            ...this.state._userErrors,
            authentication: action['failure'],
          }}); 
          break;
        }
        this.state._currentUser = action.user;
        this.state._userData = action.data;
        this.state._userBalance = action.balance;
        break;
      case ActionConstants.LOGOUT:
        this.state._currentUser = null;
        this.state._userData = {};
        this.state._userBalance = {};
        break;
      default:
        return;
    }

    this.__emitChange();
  }
}

export default new CurrentUserStore(Dispatcher);