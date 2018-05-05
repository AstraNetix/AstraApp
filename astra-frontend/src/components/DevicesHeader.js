import React from 'react'
import {Container} from 'flux/utils';
import Button from './core/Button'
import Popup from 'reactjs-popup'
import AddButton from './core/AddButton'

import CurrentUserStore from '../stores/CurrentUserStore'
import CurrentDeviceStore from '../stores/CurrentDeviceStore'
import CurrentDeviceActions from '../actions/CurrentDeviceActions'

import '../css/DeviceView.css'
import '../css/Button.css'

class DevicesHeader extends React.Component {
  static getStores() {
    return [CurrentUserStore, CurrentDeviceStore];
  }

  static calculateState(prevState) {
    return ({
      thisDevice: CurrentDeviceStore.getUID(),
      devices: CurrentUserStore.getDevices(),
    });
  }

  _deviceChange = (event) => {
    CurrentDeviceActions.changeDevice(event.target.name);
  }

  render() {
    return (
      <div className='devices-header'>
        <div style={{float: 'left', fontSize: 'xx-large'}}> Devices </div>
        <div style={{float: 'right', marginRight: '7em'}}>
          <Popup trigger={<AddButton/>} position="left bottom" closeOnDocumentClick>
            <AddDevicePopup/>
          </Popup>
          {Object.keys(this.state.devices).map((uid, index) => 
            <Button key={uid} name={uid} handleClick={this._deviceChange} style={{minWidth: '5em', paddingLeft: '2em'}}
            className={this.state.thisDevice == uid ? 'dark-link-selected' : 'dark-link'}>
              {this.state.devices[uid].name} 
            </Button>
          )}
        </div>
      </div>
    );
  }
}

class AddDevicePopup extends React.Component {
  render() {
    const selectedStyle = (platform) => {
      let isSelected = this.state.platforms[platform]
      return ({
        width: '7em',
        padding: '0.7em', 
        fontSize: '1em',
        color: isSelected ? 'rgb(230, 230, 230)' : '#646464',
        background: isSelected ? '#646464' : 'none',
      });
    }
    return (
      <div>
        Add a device
        <div className='small-detail'>
          <div> Version:  1.0</div>
          <div> Build:    98.25.6</div>
          <div> Released: 2018</div>
        </div>
        <div>
          <Button style={selectedStyle('macOS')} className='input-dark select-light'
            handleClick={this._selectMacOS}>
            macOS
          </Button>
          <Button style={selectedStyle('windows')} className='input-dark select-light' 
            handleClick={this._selectWindows}>
            Windows
          </Button>
          <Button style={selectedStyle('linux')} className='input-dark select-light'
            handleClick={this._selectLinux}>
            Linux
          </Button>
          <Button style={{padding: '0.7em', fontSize: '1em', margin: '0em 0.5em'}} 
            className='input-dark submit-light' handleClick={this._handleDownload}>
            Download
          </Button>
        </div>
      </div>  
    );
  }
}



export default Container.create(DevicesHeader);