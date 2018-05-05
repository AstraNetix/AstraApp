import React from 'react'
import Center from 'react-center'
import CurrentUserStore from '../stores/CurrentUserStore'
import Image from './core/Image'
import logo from '../images/Astra-Logo@3x.png'
import Button from './core/Button';

import '../css/Button.css'
import '../css/Welcome.css'
import '../css/index.css'

class WelcomeView extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      name: CurrentUserStore.getName().split(" ")[0],
      platforms: {
        macOS: true,
        windows : false, 
        linux: false,
      },
    };
  }

  _handleDownload = (event) => () => {
    return null;
  }

  _selectMacOS = (event) => {
    this.setState({platforms: {
      macOS: true,
      windows : false, 
      linux: false,
    }});
  }

  _selectWindows = (event) => {
    this.setState({platforms: {
      macOS: false,
      windows : true, 
      linux: false,
    }});
  }

  _selectLinux = (event) => {
    this.setState({platforms: {
      macOS: false,
      windows : false, 
      linux: true,
    }});
  }

  render() {
    const selectedStyle = (platform) => {
      let isSelected = this.state.platforms[platform]
      return ({
        width: '7em',
        padding: '0.7em', 
        fontSize: '1em',
        color: isSelected ? 'rgb(230, 230, 230)' : '#646464',
        background: isSelected ? '#646464' : 'none',
      });
    }
    return(
      <div className='welcome'>
        <Center> 
          <Button className='no-button'> 
            <Image src={logo} height={80} width={80} style={{marginTop: '1em'}}/> 
          </Button> 
        </Center>
        <div style={{fontSize: '2em', margin: '1.5em 0em 1em'}}>
          Welcome to Astra, {this.state.name}
        </div>   
        <div style={{margin: '2em 0em'}}>
          To start contributing, download the desktop client, follow the instructions for installation, 
          and login with your account.
        </div>
        <Center style={{display: 'flex', flexWrap: 'wrap'}}>
          <div className='small-detail'>
            <div> Version:  1.0</div>
            <div> Build:    98.25.6</div>
            <div> Released: 2018</div>
          </div>
          <Button style={{padding: '0.7em', fontSize: '1em', margin: '0em 0.5em'}} 
          className='input-dark submit-light'
           handleClick={this._handleDownload}>
            Download
          </Button>
          <Button style={selectedStyle('macOS')} className='input-dark select-light'
          handleClick={this._selectMacOS}>
            macOS
          </Button>
          <Button style={selectedStyle('windows')} className='input-dark select-light' 
          handleClick={this._selectWindows}>
            Windows
          </Button>
          <Button style={selectedStyle('linux')} className='input-dark select-light'
          handleClick={this._selectLinux}>
            Linux
          </Button>
        </Center>
        <div style={{margin: '2em 0em'}}>
        Through Astra, you can contribute to any project by giving a fraction of your computer’s resources 
        to a project task. You’ll also earn crypto in the process! Make sure to add your Ethereum address in the 
        profile tab to get your Stars.
        </div>
        <div style={{margin: '0em 0em'}}>
        Once you sign in, you can add projects through the projects tab. You can view device status and usage 
        settings through the devices tab. You can see your balance and contributions in the profile tab. 
        Finally, you can view your achievements and awards in the achievements tab. 
        </div>
        <Center>
          <Button className='input-light select-light' href='/devices' 
          style={{padding: '0em 8em', borderColor: '#646464', marginTop: '2em'}}>
            Got it!
          </Button>
        </Center>
      </div>
    );
  }
}

export default WelcomeView;