import React from 'react'
import Sidebar from './Sidebar'
import DeviceInfo from './DeviceInfo'

class DevicesView extends React.Component {
  render() {
    return(
      <div>
        <Sidebar />
        <DeviceInfo />
      </div>
    )
  }
}

export default DevicesView;