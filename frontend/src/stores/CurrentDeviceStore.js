import ActionConstants from '../constants/ActionConstants'
import Dispatcher from '../dispatcher'
import ServerAPI from '../ServerAPI'
import {Store} from 'flux/utils'

class CurrentDeviceStore extends Store {
  constructor(dispatcher) {
    super(dispatcher);
    this._currentDevice = null;
    this._runningProjects = null;
  }

  getCurrentDevice = () => {
    return this._currentDevice;
  }

  getRunningProjects() {
    return this._runningProjects;
  }

  __onDispatch(action) {
    if (action.status >= 300) { return; }
    switch(action.actionType) {
      case ActionConstants.LOGIN:
        this._currentDevice = action.device;
        this._runningProjects = action.projects;
        break;
      case ActionConstants.LOGOUT:
        this._currentDevice = {};
        break;  
      default:
        return;
    }

    this.__emitChange();
  }
}

export default new CurrentDeviceStore(Dispatcher);