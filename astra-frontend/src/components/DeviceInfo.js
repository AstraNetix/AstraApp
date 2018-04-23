import React from 'react'
import Image from './core/Image'

const images = {
  laptop : 1, /* laptopImage */
  desktop : 2, /*desktopImage */
  mobile : 3, /* mobileImage */
}  

class DeviceInfo extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      name : props.name, 
      model : props.model,
      processor: props.processor,
      graphics : props.graphics,
      memory : props.memory,
      type : images[props.type],   
    };
  }

  render() {
    return(
      <div className='device-info'>
        <Image src={this.state.type}/>
        <div className='device-title'> {this.state.name} </div>
        <div className='device-data'>
          <span>
            <div style='fontWeight:bold;'> Model </div> 
            {this.state.model}
          </span>
          <span>
            <div style='fontWeight:bold;'> Processor </div> 
            {this.state.processor}
          </span>
          <span>
            <div style='fontWeight:bold;'> Graphics </div> 
            {this.state.graphics}
          </span>
          <span>
            <div style='fontWeight:bold;'> Memory </div> 
            {this.state.memory}
          </span>
        </div>
      </div>
    );
  }
}

export default DeviceInfo;