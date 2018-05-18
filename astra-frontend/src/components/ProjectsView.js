import React from 'react'
import {Container} from 'flux/utils';
import ProjectsStore from '../stores/ProjectsStore'
import SearchBar from './core/SearchBar'
import Filter from './core/Filter'
import DeviceConstants from '../constants/DeviceConstants'

import '../css/ProjectsView.css'

class ProjectsView extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      projects: ProjectsStore.getProjects(),
      filtered: ProjectsStore.getProjects(),
      filters: [],
    }
  }

  static getStores() {
    return [ProjectsStore];
  }

  static calculateState(prevState) {
    return {
      projects: ProjectsStore.getProjects(),
      filtered: prevState ? prevState.filtered : [],
      filters: prevState ? prevState.filters : [],
    };
  }

  _getQueryset = () => {
    var queryset = {};
    Object.keys(this.state.projects).forEach(url => {
      queryset[this.state.projects[url].name] = {
        url: url, 
        name: this.state.projects[url].name,
        sponsors: this.state.projects[url].sponsors,
        blurb: this.state.projects[url].blurb,
        description: this.state.projects[url].description,
        area: this.state.projects[url].area,
        platforms: Object.keys(this.state.projects[url].platforms).map(platform => platform.name),
      };
    });
    return queryset;
  }

  _getFilteredProjects = (selected) => {
    let projects = this.state.projects;
    var filtered = {};
    Object.keys(projects).forEach(url => {
      selected.forEach(filter => {
        if (projects[url][filter[0]] === filter[1]) {
          return;
        }
        filtered[url] = projects[url];
      });
    });
    return filtered;
  }

  _handleFilter = (selected) => {
    this.setState({
      filtered: this._getFilteredProjects(selected),
      filters: selected,
    });
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

    const filters = {
      area: ProjectsStore.getAreas(), 
      platforms: Object.keys(DeviceConstants)
                  .map(platform => DeviceConstants[platform].name),
    };

    const contributorsStyle = (url) => {
      return {
        backgroundColor: 'rgb(' + this.state.projects[url].color.join(', ') + ')',
        borderRadius: '30px',
        padding: '0.4em 0.4em',
        width: '5em',
        color: brightness(...this.state.projects[url].color) < 130 ? 
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
          {Object.keys(this.state.filtered).map((url) => 
            <div className='project'>
              <div style={{fontSize: 'x-large', fontWeight: '400', marginBottom: '1em'}}> 
                {this.state.filtered[url].name} 
              </div>
              <div > 
                {this.state.filtered[url].blurb} 
              </div>
              <div style={{fontWeight: '500', marginTop: '0.5em', fontSize: 'medium'}}>
                Sponsors
              </div>
              <div> 
                {this.state.filtered[url].sponsors} 
              </div>
              <div>
                <div style={contributorsStyle(url)}> {this.state.filtered[url].contributors}</div>
                <div> Contributors </div>
              </div>
            </div>
          )}
        </div>
        <div style={{position: 'absolute', right: '2em'}}>
          <Filter filters={filters} handleFilter={this._handleFilter}/>
        </div>
      </div>
    );
  }
}

export default Container.create(ProjectsView);