import React from 'react'
import Image from './core/Image'
import Button from './core/Button'
import logo from '../images/Astra-Logo-White.png'
import CurrentUserActions from '../actions/CurrentUserActions'

import '../css/index.css'
import '../css/Button.css'

class TopBar extends React.Component {
  handleLogout = () => {
    CurrentUserActions.logout();
  }

  render() {
    return(
      <div className='top-bar'>
        <div style={{marginLeft: '1em'}}>
          <Button className='no-button'>
            <Image src={logo} height={30} width={30} style={{marginTop: '0.8em'}}/>
          </Button>         
        </div>
        <div style={{position: 'fixed', right: '1em', top: '0.5em'}}>
          <Button className='light-link'> Help </Button>
          <Button className='light-link'> About </Button>
          <Button className='light-link'> Request a feature </Button>
          <Button className='logout-button' handleClick={this.handleLogout}> 
            Logout 
          </Button>
        </div>
      </div>
    );
  }
}

export default TopBar