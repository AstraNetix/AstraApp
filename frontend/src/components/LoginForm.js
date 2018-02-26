import React from 'react'
import LoginButton from "./buttons/LoginButton"
import Button from "./core/Button"
import CurrentUserActions from "../actions/CurrentUserActions"
import Center from 'react-center';
import "../css/LoginForm.css"

class LoginForm extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      login: {
        email: '',
        password: '',
      }
    }
  }

  handleInputChange = (property) => (event) => {
    const { login } = this.state;
    const newLogin = {
      ...login,
      [property]: event.target.value
    };
    this.setState({ login: newLogin });
  }

  handleSubmit = (event) => {
    this.setState({loggingIn: true});
    CurrentUserActions.login(this.props.login.email, this.props.login.password);
  }

  render() {
    return(
      <Center>
        <div className='login-form'>
          <div className='login-title'>
            Login
          </div>
          <form className='login-input' onSubmit={this.handleSubmit}>
            <label> Email </label>
            <label>
              <input 
                className='input' 
                type='email'
                value={this.state.email} 
                onChange={this.handleInputChange('email')} />
            </label>
          </form>
          <form className='login-input' onSubmit={this.handleSubmit}>
            <label> Password </label>
            <label>
              <input 
                className='input' 
                type='password' 
                value={this.state.password} 
                onChange={this.handleInputChange('password')} />
            </label>
          </form>
          <LoginButton handleClick={this.handleSubmit}/>
          <Button className='gradient-border'>
            <div className='gradient-text'>
              Forgot Password
            </div>
          </Button>
        </div>
      </Center>
    )
  }
}

export default LoginForm;