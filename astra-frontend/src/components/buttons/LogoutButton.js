import React from 'react';

import Button from '../core/Button';
import CurrentUserActions from '../../actions/CurrentUserActions';
import logoutArrow from '../../images/LogoutArrow.png';
import Image from '../core/Image';

class LogoutButton extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      loggingOut: false,
    };
  }

  logout() {
    this.setState({loggingOut: true});
    CurrentUserActions.logout();
  }

  render() {
    return (
      <Button 
        className='small'
        loading={this.state.loggingOut}
        handleClick={this.logout}>
        <Image src={logoutArrow} height={15} width={15} />
        Log Out 
      </Button>
    );
  }
}

export default LogoutButton;