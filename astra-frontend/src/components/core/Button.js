import PropTypes from 'prop-types';
import React from 'react'
import {Link} from 'react-router-dom';
import '../../css/Button.css'

class Button extends React.Component {
  static propTypes = {
    className: PropTypes.string,
    loading: PropTypes.bool,
    href: PropTypes.string,
    handleClick: PropTypes.func,
  }

  render() {
    var ButtonComponent = this.props.href ? Link : 'button';

    return(
      <ButtonComponent
        {... this.props}
        className={this.props.className}
        onClick={this.props.handleClick}
        disabled={this.props.loading}
        to={this.props.href}>
        {this.props.children}
      </ButtonComponent>
    );
  }
}

export default Button;