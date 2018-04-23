'use strict'

import ActionConstants from 'constants/ActionConstants'
import Dispatcher from 'dispatcher/Dispatcher'

class CurrentDeviceActions {
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

  changeUsageTimes(deviceID, days, startTime, endTime) {
    action(ActionConstants.CHANGE_USAGE_TIMES, {deviceID: deviceID, days: days, 
      startTime: startTime, endTime: endTime});
  }

  changeCPUPercent(deviceID, percent) {
    action(ActionConstants.CHANGE_CPU_PERCENT, {deviceID: deviceID, percent: percent});
  }

  changeCPUCores(deviceID, percent) {
    action(ActionConstants.CHANGE_CPU_CORES, {deviceID: deviceID, numCores: numCores});
  }

  changeRAMPercent(deviceID, percent) {
    action(ActionConstants.CHANGE_RAM_PERCENT, {deviceID: deviceID, percent: percent});
  }

  changeDiskPercent(deviceID, percent) {
    action(ActionConstants.CHANGE_DISK_PERCENT, {deviceID: deviceID, percent: percent});
  }

  changeNetworkDown(deviceID, percent) {
    action(ActionConstants.CHANGE_NETWORK_DOWN, {deviceID: deviceID, kbps: kbps});
  }

  changeNetworkUp(deviceID, percent) {
    action(ActionConstants.CHANGE_NETWORK_UP, {deviceID: deviceID, kbps: kbps});
  }

  changeUseMemoryOnly(deviceID, opt) {
    action(ActionConstants.USE_MEMORY_ONLY, {deviceID: deviceID, opt: opt});
  }
  
  changeRunIfActive(deviceID, opt) {
    action(ActionConstants.RUN_IF_ACTIVE, {deviceID: deviceID, opt: opt});
  }

  changeRunOnBatteries(deviceID, opt) {
    action(ActionConstants.RUN_ON_BATTERIES, {deviceID: deviceID, opt: opt});
  }
}

export default CurrentDeviceActions;