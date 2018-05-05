import React from 'react'
import TopBar from './TopBar'
import LoginForm from './LoginForm'
import RegisterForm from './RegisterForm'

import '../css/index.css'
import '../css/InitialView.css'

class InitialView extends React.Component {
  render() {
    return(
      <div className='initial-view' style={{position: 'relative', left: '50%'}}>
        <TopBar />
        <RegisterForm />
        <LoginForm />
      </div>
    )
  }
}
  
export default InitialView;