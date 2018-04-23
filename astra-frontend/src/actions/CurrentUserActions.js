import ActionConstants from 'constants/ActionConstants'
import Dispatcher from 'dispatcher/Dispatcher'

class CurrentUserActions {
  action(action, args) { 
    action.method(Object.keys(args).map((key) => args[key]))
    .then((response) => {
      Dispatcher.dispatch({
        type: action.value,
        response: response,
        args: args,
      });
    });
  }

  register(name, email) {
    this.action(ActionConstants.REGISTER, {name: name, email: email})
  }

  login(email) {
    this.action(ActionConstants.LOGIN, {email: email})
  }

  logout() {
    this.action(ActionConstants.LOGOUT, {})
  }

  redirectDevices(deviceID) {
    this.action(ActionConstant.DEVICES, {})
  }

  addProject(url, deviceID) {
    this.action(ActionConstants.ADD_PROJECT, {url: url, deviceID: deviceID})
  }

  removeProject(url, deviceID) {
    this.action(ActionConstants.REMOVE_PROJECT, {url: url, deviceID: deviceID})
  }
}

export default CurrentUserActions;