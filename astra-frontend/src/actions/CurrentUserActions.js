import ActionConstants from 'constants/ActionConstants'
import Dispatcher from 'dispatcher/Dispatcher'

class CurrentUserActions {
  static action = (action, args) => { 
    action.method(Object.keys(args).map((key) => args[key]))
    .then((response) => {
      Dispatcher.dispatch({
        type: action.value,
        response: response,
        args: args,
      });
    });
  }

  static register = (name, email) => {
    CurrentUserActions.action(ActionConstants.REGISTER, {name: name, email: email})
  }

  static login = (email) => {
    CurrentUserActions.action(ActionConstants.LOGIN, {email: email})
  }

  static logout = () => {
    CurrentUserActions.action(ActionConstants.LOGOUT, {})
  }

  static redirectDevices = (deviceID) => {
    CurrentUserActions.action(ActionConstant.DEVICES, {})
  }

  static addProject = (url, deviceID) => {
    CurrentUserActions.action(ActionConstants.ADD_PROJECT, {url: url, deviceID: deviceID})
  }

  static removeProject = (url, deviceID) => {
    CurrentUserActions.action(ActionConstants.REMOVE_PROJECT, {url: url, deviceID: deviceID})
  }
}

export default CurrentUserActions;