'use strict'

import React from 'react'
import Button from "./core/Button"
import CurrentUserActions from "../actions/CurrentUserActions"
import ServerAPI from "../ServerAPI"
import Cookies from 'js-cookie';

import "../css/InitialView.css"
import "../css/Button.css"

class LoginForm extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      errors: {
        general: '',
        email: Cookies.get('email') === undefined ? '' : Cookies.get('email'),
        password: '',
      },
      email: '',
      password: '',
      loading: false,
    }
  }

  _handleChange = (event) => {
    this.setState({
      [event.target.name]: event.target.value
    });
  }

  _handleLogin = (event) => {
    this.setState({loading: true});
    ServerAPI.login(this.state.email, this.state.password).then(
      this._handleSuccess,
      this._handleFailure
    );
  }

  _handleSuccess = (responseJSON) => {
    this.setState({loading: false});
    Cookies.set('email', this.state.email)
    CurrentUserActions.login(this.state.email);
  }

  _handleFailure = (responseJSON) => {
    this.setState({
      errors: responseJSON.data,
      loading: false,
    });
  }

  render() {
    return(
      <div className='initial login'>
        <div className='initial-title'>
          Login
        </div>
        <form>
          <div> {this.state.errors.general} </div>
          <div>
            <input 
              className='input-dark true-input' type="text" name='email' value={this.state.email} 
              onChange={this._handleChange} placeholder='Email' />
          </div>
          <div>
            <input 
              className='input-dark true-input' type="password" name='password' value={this.state.password} 
              onChange={this._handleChange} placeholder='Password' />
          </div>
          <div>
            <Button  className='small-button' href='/forgot-password'>
              Forgot Password?
            </Button>
          </div>
          <div>
            <Button 
              className='input-dark submit-dark' type='submit' loading={this.state.loading} 
              handleClick={this._handleLogin}>
              Login
            </Button>
          </div>
        </form>
      </div>
    )
  }
}

export default LoginForm;