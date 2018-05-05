import React from 'react'
import {Container} from 'flux/utils';
import Slider from 'react-rangeslider'
import CurrentDeviceStore from '../stores/CurrentDeviceStore'
import CurrentDeviceActions from '../actions/CurrentDeviceActions'

import '../css/DeviceView.css'

class UsageConsole extends React.Component {
  static getStores() {
    return [CurrentDeviceStore];
  }
  static calculateState(prevState) {
    return CurrentDeviceStore.getLimits();
  }

  changeCPUPercent = (value) => CurrentDeviceActions.changeCPUPercent(CurrentDeviceStore.getUID(), value);
  changeCPUCores = (value) => CurrentDeviceActions.changeCPUCores(CurrentDeviceStore.getUID(), value);
  changeRAMPercent = (value) => CurrentDeviceActions.changeRAMPercent(CurrentDeviceStore.getUID(), value);
  changeDiskPercent = (value) => CurrentDeviceActions.changeDiskPercent(CurrentDeviceStore.getUID(), value);
  changeNetworkDown = (value) => CurrentDeviceActions.changeNetworkDown(CurrentDeviceStore.getUID(), value);
  changeNetworkUp = (value) => CurrentDeviceActions.changeNetworkUp(CurrentDeviceStore.getUID(), value);

  render() {
    return (
      <div className='usage-console'>
      <div> CPU </div>
       {/* <Slider
        value={5}
        onChangeComplete={this.changeCPUPercent}
        /> */}
        {this.state.cpu.usage}
      </div>
    );
  }
}

export default Container.create(UsageConsole);