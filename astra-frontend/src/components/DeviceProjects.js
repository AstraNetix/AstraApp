import React from 'react'
import {Container} from 'flux/utils';
import Button from "./core/Button"
import AddButton from './core/AddButton'
import CurrentDeviceStore from '../stores/CurrentDeviceStore'
import CurrentUserActions from '../actions/CurrentUserActions'

import '../css/DeviceView.css'
import '../css/Button.css'

class DeviceProjects extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      a_url: ['A project', true],
      another_url: ['Another project', true],
      yep_url: ['Yet another', false],
      let_url: ['And another', false],
      wowee: ['A superrr lonnggg project', true],
    }
  }

  static getStores() {
    return [CurrentDeviceStore];
  }

  static calculateState(prevState) {
    return CurrentDeviceStore.getProjects();
  }

  _handleSuspend = () => {
    // CurrentUserActions.suspendProject(url);
  }

  render() {
    let col1 = Object.keys(this.state).slice(0, 4);
    let col2 = Object.keys(this.state).slice(4, 8);

    const projectMini = (url, index) => {
      return (
        <div className='project-mini'>
          <Button className='dark-link' href={'/projects#'+this.state[url][0]} style={{fontSize: 'small'}}> 
            {this.state[url][0].length > 24 ? this.state[url][0].slice(0, 20) + '...' : this.state[url][0]}
          </Button>
          <Button handleClick={this._handleSuspend} className='dark-link' 
          style={{color: this.state[url][1] ?  '#d91919' : '#37c91a', float: 'right', fontSize: 'small'}}> 
            {this.state[url][1] ? 'Suspend' : 'Resume'} 
          </Button>
        </div>
      );
    }

    return (
      <div style={{fontSize: 'large', marginTop: '2em', width: '45%'}}>
        <div  style={{marginBottom: '0.5em'}}>
          Projects
          <AddButton href='/projects' type='circular'/>
        </div>
        <div style={{display: 'flex', flexWrap: 'wrap'}}>
          <div> {col1.map(projectMini)} </div>
          <div> {col2.map(projectMini)} </div>
        </div>
      </div>
    );
  }
}

export default Container.create(DeviceProjects);