import React from 'react'
import LoginButton from "./buttons/LoginButton"
import Button from "./core/Button"
import CurrentUserActions from "../actions/CurrentUserActions"

import "../css/InitialView.css"
import "../css/Button.css"

class LoginForm extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      error: '',
      email: '',
      password: '',
      loading: false,
    }
  }

  handleChange = (event) => {
    this.setState({
      [event.target.name]: event.target.value
    });
  }

  handleLogin = (event) => {
    this.setState({loggingIn: true});
    CurrentUserActions.login(this.state.email, this.state.password);
  }

  render() {
    return(
      <div className='initial login'>
        <div className='initial-title'>
          Login
        </div>
        <form>
          <div> {this.state.error} </div>
          <div>
            <input 
              className='input-dark true-input' type="text" name='email' value={this.state.email} 
              onChange={this.handleChange} placeholder='Email' />
          </div>
          <div>
            <input 
              className='input-dark true-input' type="password" name='password' value={this.state.password} 
              onChange={this.handleChange} placeholder='Password' />
          </div>
          <Button className='small-button' href='/forgot-password'>
            Forgot Password?
          </Button>
          <div>
            <Button 
              className='input-dark submit-dark' type='submit' loading={this.state.loading} 
              handleClick={this.handleLogin}>
              Login
            </Button>
          </div>
        </form>
      </div>
    )
  }
}

export default LoginForm;