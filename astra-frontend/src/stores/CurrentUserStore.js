import ActionConstants from '../constants/ActionConstants'
import Dispatcher from '../dispatcher'
import ServerAPI from '../ServerAPI'
import {Store} from 'flux/utils'
import image from '../images/Phone.png'


class CurrentUserStore extends Store {
  constructor(dispatcher) {
    super(dispatcher);
    this.state = {
      email: null,
      data: {},
      balance: {},
      devices: {},
      errors: {},
    };
  }

  getUserEmail() { 
    return this.state.email;
  }

  getSideBarState() {
    return {
      name: this.state.data.first_name + this.state.data.last_name, 
      level: 1, 
      image: this.state.data.selfie,
      stars: this.state.balance.starBalance,
    };
  }

  __onDispatch(action) {
    switch(action.actionType) {

      case ActionConstants.LOGIN:
        if (action.response.status != 200) {
          this.setState({errors: {
            ...this.state.errors,
            authentication: action['failure'],
          }}); 
          break;
        }
        this.setState({
          email: action.args.email,
          data: {
            firstName: action.response.data['first_name'],
            lastName: action.response.data['last_name'],
            profile: action.response.data['selfie'],
          },
          balance: {
            star: action.response.balance['star_balance'],
          },
          devices: ServerAPI.getUserDevices(),
        });
        break;

      case ActionConstants.LOGOUT:
        this.setState({
          email: '',
          data: {},
          balance: {},
          devices: {},
        });
        break;
      default:
        return;
    }

    this.__emitChange();
  }
}

export default new CurrentUserStore(Dispatcher);