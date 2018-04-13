import React from 'react'
import LoginForm from './LoginForm'
import RegisterForm from './RegisterForm'
import Center from 'react-center'

import '../css/index.css'
import '../css/InitialView.css'

class InitialView extends React.Component {
    render() {
      return(
        <div className='initial-view' style={{position: 'relative', left: '50%'}}>
          <RegisterForm />
          <LoginForm />
        </div>
      )
    }
  }
  
  export default InitialView;