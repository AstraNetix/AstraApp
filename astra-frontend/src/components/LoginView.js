import React from 'react';
import RegisterForm from './RegisterForm';
import LoginForm from './LoginForm';
import CurrentUserStore from '../stores/CurrentUserStore';

class LoginView extends React.Component {
  constructor(props) {
    super(props);
    this.state = {token: null};
  }

  componentDidMount() {
    this.setState({
      token: CurrentUserStore.addListener(this.handleChange),
    });
  }

  componentWillUnmount() {
    this.state.token.remove();
  }

  handleChange = (event) => {

  }

  render() {
    return(
      <div className='login'>
        <LoginForm />
      </div>
    );
  }
}

export default LoginView;