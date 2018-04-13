import React from 'react'
import LoginButton from "./buttons/LoginButton"
import Button from "./core/Button"
import CurrentUserActions from "../actions/CurrentUserActions"

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

  handleChange = (event) => {
    this.setState({
      [event.target.name]: event.target.value
    });
  }

  handleRegister = (event) => {
    this.setState({loading: true});
    CurrentUserActions.register(this.state.name, this.state.email, this.state.password, this.state.confirmPassword);
  }

  render() {
    return(
      <div className='initial register'>
        <div className='initial-title'>
          Register
        </div>
        <form className='login-form' onSubmit={this.handleRegister}>
          <div> {this.state.error} </div>
          <div>
            <input type='text' value={this.state.name} onChange={this.handleChange} 
            name='name' placeholder='Name' className='input-light true-input'/>
          </div>
          <div>
            <input type='text' value={this.state.email} onChange={this.handleChange} 
            name='email' placeholder='Email' className='input-light true-input'/>
          </div>
          <div>
            <input type='password' value={this.state.password} onChange={this.handleChange} 
            name='password' placeholder='Password' className='input-light true-input'/>
          </div>
          <div>
            <input type='password' value={this.state.confirmPassword} onChange={this.handleChange} 
            name='confirmPassword' placeholder='Confirm Password' className='input-light true-input'/>
          </div>
          <div>
            <Button className='input-light submit-light' type='submit' loading={this.state.loading} 
              handleClick={this.handleRegister}> 
              Register
            </Button>
          </div>
        </form>
      </div>
    )
  }
}

export default RegisterForm;