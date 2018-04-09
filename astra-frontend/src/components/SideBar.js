import React from 'react'
import Image from './core/Image'

import logoImage from '../images/Astra-Logo@3x.png'
import userPlaceholder from '../images/User.png'
import Button from './core/Button'
import UserTab from './UserTab'
import "../css/SideBar.css"
import Link from 'react-router-dom/Link';

class SideBar extends React.Component {
  
  render() {
    return(
      <div className="side-bar">
        <UserTab />
        <Link to="/devices/">Devices</Link>
      </div>
    );
  }
}

export default SideBar;

