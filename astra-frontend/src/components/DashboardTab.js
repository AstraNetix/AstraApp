import React from 'react'
import ReactRouter from 'react-router'
import Chart from "react-chartjs"

import MainTab from './core/MainTab.js'

import CurrentUserStore from '../stores/CurrentUserStore'
import CurrentDeviceStore from '../stores/CurrentDeviceStore'

class DashboardTab extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      currentUser: () => CurrentUserStore.getCurrentUser(),
      thisDevice: () => CurrentDeviceStore.getCurrentDevice(),
      runningProjects: () => CurrentDeviceStore.getRunningProjects(),
    };
  }

  render() {
    var currentUser, thisDevice, runningProjects;
    ({currentUser, thisDevice, runningProjects} = this.state);
    return (
      <MainTab name='Dashboard'>
        <div className='dashboard-tab'>
          
        </div>
      </MainTab>
    )
  }
}

export default DashboardTab;
