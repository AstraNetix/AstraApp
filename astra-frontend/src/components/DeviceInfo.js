import React from 'react'
import {Container} from 'flux/utils';
import Image from './core/Image'
import CurrentDeviceStore from '../stores/CurrentDeviceStore'
import laptop from '../images/Laptop.png'
import '../css/DeviceView.css'

const images = {
  laptop : laptop,
  desktop : 2, /*desktopImage */
  mobile : 3, /* mobileImage */
}  

class DeviceInfo extends React.Component {
  static getStores() {
    return [CurrentDeviceStore];
  }

  static calculateState(prevState) {
    return CurrentDeviceStore.getInfo();
  }

  render() {
    return(
      <div className='device-info'>
        <div style={{padding: '1em 0em', marginRight: '1.5em'}}>
          <Image  src={images[this.state.type]} width={200} height={116}/>
        </div>
        <div>
          <div style={{fontSize: 'x-large', marginBottom: '0.5em'}}> {this.state.name} </div>
          <table>
            <trbody>
            <tr>
              <td style={{fontWeight: '400'}}> Model </td>
              <td>{this.state.model}</td>
            </tr>
            <tr>
              <td style={{fontWeight: '400'}}> Processor </td>
              <td>{this.state.processor}</td>
            </tr>
            <tr>
              <td style={{fontWeight: '400'}}> Graphics </td>
              <td>{this.state.graphics}</td>
            </tr>
            <tr>
              <td style={{fontWeight: '400'}}> Memory </td>  
              <td>{this.state.memory}</td>
            </tr>
            </trbody>
          </table>
        </div>
      </div>
    );
  }
}

export default Container.create(DeviceInfo);