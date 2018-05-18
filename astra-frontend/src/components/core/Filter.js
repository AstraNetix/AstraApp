import React from 'react'
import Button from './Button'
import ExternalClicker from './ExternalClicker'
// import ReactCSSTransitionGroup from 'react-addons-css-transition-group';

import '../../css/Button.css'
import '../../css/index.css'

class Filter extends React.Component {
  constructor(props) {
    super(props);

    var filters = {};
    Object.keys(this.props.filters).forEach(filter => {
      filters[filter] = {All: true};
      this.props.filters[filter].forEach(option => {
        filters[filter][option] = true;
      });
    });

    this.state = {
      handleFilter: this.props.handleFilter,
      filters: filters,
      testSelected: [],
      focused: false,
    };
  }

  _handleClose = () => {
    this.setState({focused: false});
    this.props.handleFilter(this._getSelected());
  }

  _handleBarClick = (event) => {
    this.setState({focused: true});
  }

  _handleOptionClick = (filter, option) => {
    if (option === 'All') {
      return this._handleAllClick(filter);
    }

    var filters = this.state.filters;
    filters[filter][option] = !filters[filter][option];
    this.setState(filters);
  }

  _handleAllClick = (filter) => {
    var newFilters = Object.assign({}, this.state.filters);
    newFilters[filter] = {All: !this.state.filters[filter].All};
    Object.keys(this.state.filters[filter]).forEach(option => {
      newFilters[filter][option] = newFilters[filter].All ? true : false;
    });
    this.setState({filters: newFilters})
  }

  _getSelected = () => {
    let selected = [].concat(...Object.keys(this.state.filters).map(filter => {
      return this.state.filters[filter].All ? 
      [] : Object.keys(this.state.filters[filter]).map(option => {
        return !this.state.filters[filter][option] ? 
          false : 
          [filter, option]
      });
    })).filter(Boolean);
    return selected;
  }

  render() {
    const selected =  {
      fontSize: '0.9em x-small',
      backgroundColor: 'rgb(238, 238, 238)',
      color: '#646464',
      padding: '5px',
    };

    const FilterBox = () => {
      return (
        <div className='filter-box'>
          {Object.keys(this.state.filters).map(filter => 
            <div style={{marginBottom: '1em'}}>
              <div style={{margin: '1em 0em 0.3em'}}>
                {filter[0].toUpperCase() + filter.substr(1)}
              </div>
              <div style={{display: 'flex', flexWrap: 'wrap'}}>
                {Object.keys(this.state.filters[filter]).map(option => 
                  <Button className='filter-button' handleClick={() => this._handleOptionClick(filter, option)} 
                    style={this.state.filters[filter][option] ? selected : {}}>
                    {option}
                  </Button>
                )}
              </div>
            </div>
          )}
        </div>
      );
    }

    const container = {
      boxShadow: this.state.focused ? '0px 3px 20px 0px rgba(31, 31, 31, 0.34)' : 'none',
      borderRadius: '5px',
      backgroundColor: this.state.focused ? '#949494' : 'none',
      borderBottomLeftRadius: '5px',
      borderBottomRightRadius: '5px',
    };

    const filterBar = {
      display: 'flex',
      flexWrap: 'wrap',
      color: this.state.focused ? 'rgb(238, 238, 238)' : '#646464',
      border: this.state.focused ? 'none' : '1px solid #646464',
      backgroundColor: this.state.focused ? 'rgba(80, 80, 80, 0.7' : 'rgba(0, 0, 0, 0)',
      width: this.state.focused ? '25em' : '2.3em',
    };

    return(
      <ExternalClicker handleClose={this._handleClose}>
        <div style={container}>
          <div style={filterBar} className='filter-bar' onClick={this._handleBarClick}>
            {!this.state.focused ? 
              'Filter' :
              this._getSelected().map((pair, index) => {
                if (index < 3) {
                  return (
                    <div style={selected} className='filter-button'>
                      {pair[1]}
                      <Button className='no-button' handleClick={() => this._handleOptionClick(pair[0], pair[1])}>
                        X
                      </Button>
                    </div>
                  );
                }
              })
            }
          </div>
          {/* <ReactCSSTransitionGroup
            transitionEnterTimeout={500}
            transitionLeaveTimeout={300}> */}
          {this.state.focused ? <FilterBox/> : null}
          {/* </ReactCSSTransitionGroup> */}
        </div>
      </ExternalClicker>
    );
  }
} 

export default Filter;