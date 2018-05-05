import React from 'react'
import Button from "./core/Button"
import CurrentUserActions from "../actions/CurrentUserActions"
import ServerAPI from '../ServerAPI'
import Cookies from 'js-cookie';

import "../css/InitialView.css"
import "../css/Button.css"

class RegisterForm extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      error: '',
      name: '',
      email: '',
      password: '',
      confirmPassword: '',
      loading: false,
    }
  }

  _handleChange = (event) => {
    this.setState({
      [event.target.name]: event.target.value
    });
  }

  _handleRegister = (event) => {
    this.setState({loading: true});
    ServerAPI.createUser(this.state.name, this.state.email, this.state.password, this.state.confirmPassword).then(
      this._handleSuccess,
      this._handleFailure
    )
  }

  _handleSuccess = (responseJSON) => {
    Cookies.set('email', this.state.email)
    CurrentUserActions.register(this.state.name, this.state.email);
  }

  _handleFailure = (responseJSON) => {
    this.setState({
      errors: responseJSON.data, 
      loading: false
    })
  }

  render() {
    return(
      <div className='initial register'>
        <div className='initial-title'>
          Register
        </div>
        <form className='login-form' onSubmit={this._handleRegister}>
          <div> {this.state.error} </div>
          <div>
            <input type='text' value={this.state.name} onChange={this._handleChange} 
            name='name' placeholder='Name' className='input-light true-input'/>
          </div>
          <div>
            <input type='text' value={this.state.email} onChange={this._handleChange} 
            name='email' placeholder='Email' className='input-light true-input'/>
          </div>
          <div>
            <input type='password' value={this.state.password} onChange={this._handleChange} 
            name='password' placeholder='Password' className='input-light true-input'/>
          </div>
          <div>
            <input type='password' value={this.state.confirmPassword} onChange={this._handleChange} 
            name='confirmPassword' placeholder='Confirm Password' className='input-light true-input'/>
          </div>
          <div>
            <Button className='input-light submit-light' type='submit' loading={this.state.loading} 
              handleClick={this._handleRegister}> 
              Register
            </Button>
          </div>
        </form>
      </div>
    )
  }
}

export default RegisterForm;