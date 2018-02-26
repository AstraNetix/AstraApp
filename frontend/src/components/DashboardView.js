import React from 'react'

import DashboardTab from './DashboardTab'
import UserTab from './UserTab'

class DashboardView extends React.Component {
  componentWillMount() {  
  }

  componentWillUnmount() {
  }

  render() {
    return (
      <div className="dashboard-view">
        <DashboardTab /> 
        <UserTab />
        {/* Add 
          <ProjectTab>
          <DeviceTab>
        to this render */}
      </div>
    );
  }
}

export default DashboardView;
