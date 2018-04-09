import React from 'react';
import Image from './core/Image';

import LogoutButton from './buttons/LogoutButton';
import Button from './core/Button';
import settingsImage from '../images/Settings Image.png';
import userPlaceholder from '../images/User.png';
import ranking from '../images/Ranking.png';

import CurrentUserStore from '../stores/CurrentUserStore';

import "../css/UserTab.css"

class UserTab extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      currentUser: null,
      userData: {
        name: "------",
        image: userPlaceholder,
        starBalance: "--",
        level: ["0", ]
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
              <span className="user-level">
                <Image className="user-image" src={this.state.userData["image"]} alt="userImage" height={30} width={30}/>
                {this.state.userData["name"]}
              </span>
            </li>
            <li>
              Balance
              <div className="balance">
                {this.state.userData["starBalance"]}
              </div>
            </li>
          </ul>
        </div>
      </div>
    );
  }
}

export default UserTab;