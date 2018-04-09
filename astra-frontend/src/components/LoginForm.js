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
      register: {
        name: '',
        email: '',
        password: '',
        confirmPassword: '',
      },
      login: {
        email: '',
        password: '',
      }
    }
  }

  handleChange = (property) => (event) => {
    const { login } = this.state;
    const { register } = this.state;
    const newRegister = {
      ...register,
      [property]: event.target.value
    }
    const newLogin = {
      ...login,
      [property]: event.target.value
    };
    this.setState({ login: newLogin , register: newRegister});
  }

  handleLogin = (event) => {
    this.setState({loggingIn: true});
    CurrentUserActions.login(this.props.login.email, this.props.login.password);
  }

  handleRegister = (event) => {
    this.setState({registering: true});
    CurrentUserActions.register(this.props.login.email, this.props.login.password);
  }

  render() {
    return(
      <Center>
        <div className='register'>
          Register
          <form className='login-form'>
            <input type="text" value={this.state.register.name} onChange={this.handleChange} />
          </form>
        </div>
      </Center>
    )
  }
}

export default LoginForm;