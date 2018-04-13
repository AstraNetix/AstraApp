import React from 'react'

class MainTab extends React.Component {
  render() {
    return (
      <div className="main-tab">
        {this.props.name}
        <div className='main-children'>
          {this.props.children}
        </div>
      </div>
    );
  }
}

export default MainTab;
