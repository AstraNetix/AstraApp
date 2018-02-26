import React from 'react'
import Image from './core/Image'

import logoImage from '../images/Astra-Logo@3x.png'
import Button from './core/Button'
import "../css/TopBar.css"

class TopBar extends React.Component {
  render() {
    return(
      <div className="top-bar">
        <div className = "top-container">
          <Button className="clear" href=""> {/* TODO: Add link to Astra Homepage */} 
            <Image src={logoImage} width={30} height={30} alt="logoImage" />
          </Button>
          <div className="top-text">
            Astra
          </div>
        </div>
        <div className="top-text">
          <Button className="medium" href=""> {/* TODO: Add link to Help and Support page */} 
            Help and Support
          </Button>
          <Button className="medium" href=""> {/* TODO: Add link to Astra About page */} 
            About Us
          </Button>
        </div>
      </div>
    );
  }
}

export default TopBar;

