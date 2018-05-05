import ActionConstants from '../constants/ActionConstants'
import DeviceConstants from '../constants/DeviceConstants'
import Dispatcher from '../dispatcher'
import ServerAPI from '../ServerAPI'
import {Store} from 'flux/utils'
import userProfile from '../images/User.png'
import cookie from "react-cookie";

class CurrentUserStore extends Store {
  constructor(dispatcher) {
    super(dispatcher);
    this.email = null;
    this.data = {
      firstName: 'Soham',
      lastName: 'Kale',
      profile: userProfile,
      level: 1,
    };
    this.balance = {
      stars: '$0.00',
    };
    this.devices = {
      1: {name: 'A device', platform: DeviceConstants.WINDOWS},
      2: {name: 'Another device', platform: DeviceConstants.MACOS},
      3: {name: 'A third device', platform: DeviceConstants.LINUX},
    }; // {uid: {name, platform}}
  }

  getErrors() { return this.errors; }

  getUserEmail() {  return this.email; }

  getDevices() { return this.devices; }
  
  getName() { return (this.data.firstName + ' ' + this.data.lastName); }

  getSideBarState() {
    return ({
      name: this.data.firstName + ' ' + this.data.lastName, 
      level: this.data.level, 
      profile: this.data.profile,
      stars: this.balance.stars,
    });
  }

  __onDispatch(action) {
    switch(action.type) {
      case ActionConstants.LOGIN:
        this.email = action.args.email;
        this.data = {
            firstName: action.response.data['first_name'],
            lastName: action.response.data['last_name'],
            profile: action.response.data['selfie'],
            /* Get level as well */
        };
        this.balance = {
          star: action.response.balance['star_balance'],
        };
        this.devices = ServerAPI.getUserDevices();
        cookie.save('email', this.email, '/');
        break;
      case ActionConstants.LOGOUT:
        break;
      default:
        return;
    }

    this.__emitChange();
  }
}

export default new CurrentUserStore(Dispatcher);