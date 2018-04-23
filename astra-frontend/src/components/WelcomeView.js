import React from 'react'
import CurrentUserStore from '../stores/CurrentUserStore'

import '../css/Button.css'
import Button from './core/Button';

class WelcomeView extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      name: CurrentUserStore.getName(),
      platform: {
        macOS: true,
        windows : false, 
        linux: false,
      },
    };
  }

  _handleDownload = () => {
    return null;
  }

  render() {
    return(
      <div>
        <div className='title'>
          Welcome to Astra, {this.state.name}
        </div>   
        To start contributing, download the desktop client, follow the instructions for installation, 
        and login with your account.
        <span>
          <div className='small dark'>
            <div> Version: </div>
            <div> Build: </div>
            <div> Released: </div>
          </div>
          <Button className='submit-light' handleClick={this._handleDownload} >
            Download
          </Button>
          <Button className={this.state.macOS ? 'select-light' : 'selected-light'} 
          handleClick={this._handleDownload} >
            macOS
          </Button>
          <Button className={this.state.windows ? 'select-light' : 'selected-light'} 
          handleClick={this._handleDownload} >
            Windows
          </Button>
          <Button className={this.state.linux ? 'select-light' : 'selected-light'} 
          handleClick={this._handleDownload} >
            Linux
          </Button>
        </span>
        Through Astra, you can contribute to any project by giving a fraction of your computer’s resources 
        to a project task. You’ll also earn crypto in the process! Make sure to add your ether address in the 
        profile tab to get your Stars.

        Once you sign in, you can add projects through the projects tab. You can view device status and usage 
        settings through the devices tab. You can see your balance and contributions in the profile tab. 
        Finally, you can view your achievements and awards in the achievements tab. 
        <Button className='select-light' href='/devices' >
          Got it!
        </Button>
      </div>
    );
  }
}

export default WelcomeView;