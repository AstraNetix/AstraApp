import React from 'react'
import Sidebar from '../Sidebar'
import DevicesView from '../DevicesView'
import WelcomeView from '../WelcomeView'
/* import ProfileView from '../ProfileView' */
/* import ProjectsView from '../ProjectsView */


class Dashboard extends React.Component {
  render() {
    const views = {
      'welcome': <WelcomeView/>,
      'devices': <DevicesView/>
    }

    return(
      <div className='dashboard'>
        <Sidebar />
        {views[this.props.type]}
      </div>
    );
  }
}

export default Dashboard;