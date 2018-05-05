import React from 'react'
import TopBar from '../TopBar'
import Sidebar from '../Sidebar'
import DevicesView from '../DevicesView'
import WelcomeView from '../WelcomeView'
/* import ProfileView from '../ProfileView' */
import ProjectsView from '../ProjectsView'

import '../../css/index.css'

const views = {
  'welcome': <WelcomeView />,
  'devices': <DevicesView />,
  // 'profile': <ProfileView />,
  'projects': <ProjectsView />,
}

class Dashboard extends React.Component {
  render() {
    return(
      <div className='dashboard'>
        <Sidebar type={this.props.type}/>
        <div>
          <TopBar />
          {views[this.props.type]}
        </div>
      </div>
    );
  }
}

export default Dashboard;