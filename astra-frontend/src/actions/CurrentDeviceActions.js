import ActionConstants from '../constants/ActionConstants'
import Dispatcher from '../dispatcher'

class CurrentDeviceActions {
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

  static changeDevice(uid) {
    CurrentDeviceActions.action(ActionConstants.DEVICE_CHANGE, {uid: uid});
  }

  static changeUsageTimes = (uid, days, startTime, endTime) => {
    CurrentDeviceActions.action(ActionConstants.CHANGE_USAGE_TIMES, {uid: uid, days: days, 
      startTime: startTime, endTime: endTime});
  }

  static changeCPUPercent = (uid, percent) => {
    CurrentDeviceActions.action(ActionConstants.CHANGE_CPU_PERCENT, {uid: uid, percent: percent});
  }

  static changeCPUCores = (uid, numCores) => {
    CurrentDeviceActions.action(ActionConstants.CHANGE_CPU_CORES, {uid: uid, numCores: numCores});
  }

  static changeRAMPercent = (uid, percent) => {
    CurrentDeviceActions.action(ActionConstants.CHANGE_RAM_PERCENT, {uid: uid, percent: percent});
  }

  static changeDiskPercent = (uid, percent) => {
    CurrentDeviceActions.action(ActionConstants.CHANGE_DISK_PERCENT, {uid: uid, percent: percent});
  }

  static changeNetworkDown = (uid, kbps) => {
    CurrentDeviceActions.action(ActionConstants.CHANGE_NETWORK_DOWN, {uid: uid, kbps: kbps});
  }

  static changeNetworkUp = (uid, kbps) => {
    CurrentDeviceActions.action(ActionConstants.CHANGE_NETWORK_UP, {uid: uid, kbps: kbps});
  }

  static changeUseMemoryOnly = (uid, opt) => {
    CurrentDeviceActions.action(ActionConstants.USE_MEMORY_ONLY, {uid: uid, opt: opt});
  }
  
  static changeRunIfActive = (uid, opt) => {
    CurrentDeviceActions.action(ActionConstants.RUN_IF_ACTIVE, {uid: uid, opt: opt});
  }

  static changeRunOnBatteries = (uid, opt) => {
    CurrentDeviceActions.action(ActionConstants.RUN_ON_BATTERIES, {uid: uid, opt: opt});
  }
}

export default CurrentDeviceActions;