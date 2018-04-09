import React from 'react'
import LoginButton from "./buttons/LoginButton"
import Button from "./core/Button"
import CurrentUserActions from "../actions/CurrentUserActions"
import Center from 'react-center';
import "../css/LoginForm.css"

class RegisterForm extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      name: '',
      email: '',
      password: '',
      confirmPassword: '',
    }
  }

  handleNameChange = (name) => {
    this.setState({name});
  }

  handleEmailChange = (email) => {
    this.setState({email});
  }

  handlePasswordChange = (password) => {
    this.setState({password});
  }

  handleConfirmPasswordChange = (confirmPassword) => {
    this.setState({confirmPassword});
  }

  handleRegister = (event) => {
    this.setState({registering: true});
    CurrentUserActions.register(this.props.login.email, this.props.login.password);
  }

  render() {
    return(
      <div className='register'>
        Register
        <form className='login-form' onSubmit={this.handleRegister}>
          <input type="text"      value={this.state.register.name}            onChange={this.handleNameChange}            />
          <input type="text"      value={this.state.register.email}           onChange={this.handleEmailChange}           />
          <input type="password"  value={this.state.register.password}        onChange={this.handlePasswordChange}        />
          <input type="password"  value={this.state.register.confirmPassword} onChange={this.handleConfirmPasswordChange} />
          <input type="submit"    value="Register" />
        </form>
      </div>
    )
  }
}

export default RegisterForm;