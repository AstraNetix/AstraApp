import React from 'react'
import Button from "../core/Button"

class LoginButton extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      loggingIn: false,
    };
  }

  render() {
    return(
      <Button 
        className='gradient' 
        href="./dashboard"
        handleClick={this.props.handleClick}>
        Submit
      </Button>
    );
  }
}

export default LoginButton;