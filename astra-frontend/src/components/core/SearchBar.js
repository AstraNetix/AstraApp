import React from 'react'
import Button from './Button'
import '../../css/index.css'

class SearchBar extends React.Component {
  /** A searchbar component that searches through a given queryset
   *  Proptypes: 
   *    queryset := [Object] A queryset of style {name => primitives, or object/array recursively 
   *                containing primitives}
   *    placeholder := [String] A placeholder in the search bar
   *    width := [int] A pixel value for width of search bar
   *    handleClick := [function] A callback function for when a result is clicked
   *    priorities := [Object] A mapping between keys in the queryset and their priority in returning 
   *                search results. No mapping for a key means 0 priority
   *    maxLevel := Deepest level to search in the queryset
   */

  constructor(props) {
    super(props);
    this.state = {
      placeholder: props.placeholder || '',
      loading: false,
      queryset: this.props.queryset, 
      priorities: this.props.priorities || {},
      results: [], 
      value: "",
      maxLevel: this.props.maxLevel || Number.MAX_SAFE_INTEGER,
      focused: false,
    };
  }

  _searcher = (item, level = 1) => {
    /** Searches recursively through this.state.queryset. Returns all matched queries as well as 
     * the depth at which it was found, which is factored into the match's importance
     * Returns an array of type [item [primitive], depth [int]]
    */
    if (level > this.state.maxLevel) { return false; }

    const flatten = array => array.reduce((a, b) => a.concat(Array.isArray(b) ? flatten(b) : b), []);

    if (typeof(item) === "string") {
      return String(item.toLowerCase()).includes(this.state.value.toLowerCase()) ? 
        {item: item, level: level} : 
        false;
    } else if (typeof(item) === "number") {
      return item === parseInt(this.state.value.toLowerCase()) ? 
        {item: item, level: level} : 
        false;
    } else if (Array.isArray(item)) {
      return flatten(item.map(item => this._searcher(item, level++)).filter(Boolean));
    } else if (typeof(item) === 'object') {
      return flatten(Object.values(item).map(item => this._searcher(item, level++)).filter(Boolean));
    } else {
      return false;
    }
  }

  _priority = (m, n) => {
    /** Takes in two items from the 'items' value for a match  */
    const priority = (item) => (item in this.state.priorities) ? this.state.priorities : 0;
    return priority(m.item) >= priority(n.item) || m.depth > n.depth;
  }

  _calculateResults = () => {
    if (!this.state.value) { return []; }

    /* For each name in queryset, find all matches in its data */
    let results = Object.keys(this.state.queryset).map(name => { 
                    return {name: name, items: this._searcher(this.state.queryset[name])}; 
                  });

    /* Delete all falsy values from the results */
    results.forEach((match, index) => {
      if (!match.items) { results.splice(index, 1); }
    });

    if (results == false) { return results; }

    /* Reduce all matched objects to a singular, most relevant value to display */
    results = results.map(match => {
      return {name: match.name, items: match.items.reduce(this._priority)};
    });
    
    /* Sort the remaining names by their item's priority */
    results.sort((m, n) => this._priority(m.items, n.items));

    return results;
  }

  _handleChange = (event) => {    this.setState({
      value: event.target.value,
      loading: true
    });
    this.setState({
      results: this._calculateResults(),
      loading: false
    })
  }
  
  render() {
    const hasInput = () => this.state.value
    const handleFocus = (event) => this.setState({focused: true});
    const handleBlur = (event) => this.setState({focused: false});

    const Results = ({style}) => {
      if (!this.state.focused || this.state.results == false) {
        return null;
      }
      return(
        <div style={style}>
          {this.state.results.map((result) =>
            <div>
              <Button handleClick={this.props.handleClick}>
                {result.item}
              </Button>
            </div>
          )}
        </div>
      );
    }

    var containerStyle = {
      marginBottom: '3em', 
      boxShadow: this.state.focused ? '0px 3px 10px 0px rgba(31, 31, 31, 0.15)' : 'none',
      width: this.props.width + 2 || '32em',
      borderRadius: '15px',
      borderBottomLeftRadius: this.state.focused && hasInput() ? '5px' : '15px',
      borderBottomRightRadius: this.state.focused && hasInput() ? '5px' : '15px',
      transition: 'all 0.2s ease',
    }

    var searchBoxStyle = {
      width: this.props.width || '30em',
      borderColor: this.state.focused ? 'rgb(243, 243, 243)' : '#838383',
      borderBottomColor: '#838383',
      borderRadius: '15px',
      borderBottomLeftRadius: this.state.focused && hasInput() ? '0px' : '15px',
      borderBottomRightRadius: this.state.focused && hasInput() ? '0px' : '15px',
      background: this.state.focused ? 'rgb(243, 243, 243)' : 'none',
      transition: 'all 0.2s ease',
      margin: '0px',
    };

    var resultsStyle = {
      width: this.props.width || '30em',
      backgroundColor: 'rgb(243, 243, 243)',
      borderColor: '#838383', 
      borderBottomLeftRadius: '5px',
      borderBottomRightRadius: '5px',
      transition: 'all 0.2s ease',
      padding: '1em',
    };

    return(
      <div style={containerStyle}>
        <form>
          <input className='input-light true-input' onChange={this._handleChange} type='text'
          placeholder={this.state.placeholder} value={this.state.value} 
          style={searchBoxStyle} onFocus={handleFocus} onBlur={handleBlur}/>
        </form>
        <Results style={resultsStyle}/>
      </div>
    );
  }
}

export default SearchBar;