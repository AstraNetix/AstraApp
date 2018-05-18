import React from 'react'

class ExternalClicker extends React.Component {
  componentDidMount() {
    document.addEventListener('mousedown', this._handleClose);
  }

  componentWillUnmount() {
    document.removeEventListener('mousedown', this._handleClose);
  }

  _setWrapperRef = (node) => {
    this.wrapperRef = node;
  }

  _handleClose = (event) => {
    if (this.wrapperRef && !this.wrapperRef.contains(event.target)) {
      this.props.handleClose();
    }
  }

  render() {
    return(
      <div ref={this._setWrapperRef}>
        {this.props.children}
      </div>
    );
  }
}

export default ExternalClicker;