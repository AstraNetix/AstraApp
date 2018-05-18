import React from 'react'
import {Container} from 'flux/utils';
import Image from './core/Image'
import DevicesIcon from '../images/DevicesIcon.png'
import ProfileIcon from '../images/ProfileIcon.png'
import ProjectsIcon from '../images/ProjectsIcon.png'
import AchievementsIcon from '../images/AchievementsIcon.png'
// import throttle from 'lodash.throttle';

import CurrentUserStore from '../stores/CurrentUserStore'

import "../css/SideBar.css"
import "../css/Button.css"
import Link from 'react-router-dom/Link';

class Sidebar extends React.Component {
  constructor(props) {
    super(props);
    this.state = CurrentUserStore.getSideBarState();
    this.state.type = this.props.type;
    this.state.isMobile = window.innerWidth < 700;
  }

  static getStores() {
    return [CurrentUserStore];
  }

  static calculateState(prevState) {
    prevState = prevState || {};
    return Object.assign(prevState, CurrentUserStore.getSideBarState());
  }

  onWindowResize = () => {
    this.setState({ isMobile: window.innerWidth < 700 });
  }

  componentDidMount() {
    window.addEventListener('resize', this.onWindowResize);
  }

  componentWillUnmount() {
    window.removeEventListener('resize', this.onWindowResize);
  }

  render() {
    const selected = (type) => 'dark-link' + (this.state.type === type ? '-selected' : '');
    return(
      <div className='side-bar' style={{width: this.state.isMobile ? '3em' : '8em', paddingLeft: this.state.isMobile ? '1em' : '2em'}}>
        <div className='user-tab'>
          <Image src={this.state.profile} height={this.state.isMobile ? 35 : 50} width={this.state.isMobile ? 35 : 50}  
            style={{borderRadius: '50%', marginBottom: '1em', boxShadow: '0px 5px 35px 0px rgba(31, 31, 31, 0.22)'}}/>  
          {this.state.isMobile ? null : <div style={{fontSize: 'large'}}> {this.state.name} </div>}
          <div> {this.state.isMobile ? 'Lvl' : 'Level' } {this.state.level} </div>
          {this.state.isMobile ? null :
            <div style={{marginTop: '2em'}}> 
              <div> Balance </div>
              <div style={{marginTop: '0.5em', fontSize: 'large'}}> {this.state.stars} </div>
            </div>
          }
        </div>
        <div className='navigation'>
          <div>
            <Link className={selected('devices')} to='/devices'> 
              {this.state.isMobile ? <Image src={DevicesIcon} height={30} width={30} style={{marginBottom: '1em'}}/> 
                : 'Devices'} 
            </Link>
          </div>
          <div>
            <Link className={selected('profile')} to='/profile'> 
              {this.state.isMobile ? <Image src={ProfileIcon} height={30} width={30} style={{marginBottom: '1em'}}/> 
                : 'Profile'} 
            </Link>
          </div>
          <div>
            <Link className={selected('projects')} to='/projects'> 
              {this.state.isMobile ? <Image src={ProjectsIcon} height={30} width={30} style={{marginBottom: '1em'}}/> 
              : 'Projects'} 
            </Link>
          </div>
          <div>
            <Link className={selected('achievements')} to='/achievements'> 
              {this.state.isMobile ? <Image src={AchievementsIcon} height={30} width={30} style={{marginBottom: '1em'}}/> 
              : 'Achievements'} 
            </Link>
          </div>
        </div>
      </div>
    );
  }
}

export default Container.create(Sidebar);