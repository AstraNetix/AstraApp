import React from 'react'
import Image from './core/Image'
import user from '../images/User.png'
import Button from './core/Button'

import CurrentUserStore from '../stores/CurrentUserStore'

import "../css/SideBar.css"
import Link from 'react-router-dom/Link';

class Sidebar extends React.Component {
  constructor(props) {
    super(props);
    this.state = CurrentUserStore.getSideBarState();
  }

  render() {
    return(
      <div className='side-bar'>
        <div className='user-tab'>
          <Image src={this.state.image} />  
          <div className='user-name'> {this.state.name} </div>
          <div className='user-level'> Level {this.state.level} </div>
          <div className='user-balance'>
            Balance
            {this.state.stars}
          </div>
        </div>
        <div>
          <Link className='dark link' href='/devices'> Devices </Link>
          <Link className='dark link' href='/profile'> Profile </Link>
          <Link className='dark link' href='/projects'> Projects </Link>
          <Link className='dark link' href='/achievements'> Achievements </Link>
        </div>
      </div>
    );
  }
}

export default Sidebar;