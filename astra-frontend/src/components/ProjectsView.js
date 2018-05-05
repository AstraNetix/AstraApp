import React from 'react'
import {Container} from 'flux/utils';
import ProjectsStore from '../stores/ProjectsStore'
import SearchBar from './core/SearchBar'

import '../css/ProjectsView.css'

class ProjectsView extends React.Component {
  static getStores() {
    return [ProjectsStore];
  }

  static calculateState(prevState) {
    return ProjectsStore.getProjects();
  }

  _getQueryset = () => {
    var queryset = {};
    Object.keys(this.state).forEach(url => {
      queryset[this.state[url].name] = {
        url: url, 
        name: this.state[url].name,
        sponsors: this.state[url].sponsors,
        blurb: this.state[url].blurb,
        description: this.state[url].description,
        area: this.state[url].area,
        platforms: Object.keys(this.state[url].platforms).map(platform => platform.name),
      };
    });
    return queryset;
  }

  _handleSelect = (event) => {
    return;
  }

  render() {
    const brightness = (r, g, b) => Math.sqrt(
      0.241*Math.pow(r, 2) +
      0.691*Math.pow(g, 2) +  
      0.068*Math.pow(b, 2)
    );

    const priorities = {
      name: 7,
      url: 6,
      area: 5, 
      blurb: 4, 
      sponsors: 3,
      description: 2,
      platforms: 1, 
    };

    const contributorsStyle = (url) => {
      return {
        backgroundColor: 'rgb(' + this.state[url].color.join(', ') + ')',
        borderRadius: '30px',
        padding: '0.4em 0.4em',
        width: '5em',
        color: brightness(...this.state[url].color) < 130 ? 
          'rgb(243, 243, 243' : 
          'rgba(80, 80, 80, 0.8)',
      }
    };

    return(
      <div className='projects-view'>
        <div style={{position: 'absolute'}}>
          <SearchBar queryset={this._getQueryset()} placeholder='Search by name, area, etc.'
            priorities={priorities}/>
        </div>
        <div className='projects-grid'>
          {Object.keys(this.state).map((url) => 
            <div className='project'>
              <div style={{fontSize: 'x-large', fontWeight: '400', marginBottom: '1em'}}> {this.state[url].name} </div>
              <div > {this.state[url].blurb} </div>
              <div style={{fontWeight: '500', marginTop: '0.5em', fontSize: 'medium'}}>Sponsors</div>
              <div> {this.state[url].sponsors} </div>
              <div>
                <div style={contributorsStyle(url)}> {this.state[url].contributors}</div>
                <div> Contributors </div>
              </div>
            </div>
          )}
        </div>
      </div>
    );
  }
}

export default Container.create(ProjectsView);