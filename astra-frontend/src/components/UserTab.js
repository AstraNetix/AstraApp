import React from 'react';
import Image from './core/Image';

import LogoutButton from './buttons/LogoutButton';
import ArrowButton from './buttons/ArrowButton'
import Button from './core/Button';
import settingsImage from '../images/Settings Image.png';
import blankUser from '../images/User Layers.png';

import CurrentUserStore from '../stores/CurrentUserStore';

import "../css/UserTab.css"

class UserTab extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      currentUser: null,
      userData: {
        name: "------",
        image: blankUser,
        starBalance: "--",
        earningRate: "--",
      },
    };
  }

  componentDidMount() {
    this._userToken = CurrentUserStore.addListener(() => {
      this.setState({
        currentUser: CurrentUserStore.getCurrentUser(),
        userData: CurrentUserStore.getUserPanelData(),
      });
    });
  }

  componentWillUnmount() {
    this._userToken && this._userToken.remove();
  }

  render() {
    return(
      <div>
        <div className="user-panel">
          <ul>
            <li>
              <Image className="user-image" src={this.state.userData["image"]} alt="userImage" height={30} width={30}/>
              {this.state.userData["name"]}
            </li>
            <li>
              Balance
              <div>
                {this.state.userData["starBalance"]}
              </div>
            </li>
            <li>
              Earning Rate
              <div>
                {this.state.userData["earningRate"]}
              </div>
            </li>
            <li>
              <ArrowButton to="/balance">
                View My Earnings
                {/* Add arrow image */}
              </ArrowButton>
            </li>
            <li>
              <Button className='small' to="/account">
                <Image src={settingsImage} height={15} width={15} />
                Settings
              </Button>
            </li>
            <li>
              <LogoutButton />
            </li>
          </ul>
        </div>
      </div>
    );
  }
}

export default UserTab;