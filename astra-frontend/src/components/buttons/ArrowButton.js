import React from 'react';
import Button from '../core/Button'
import arrowImage from '../../images/arrow.png'
import Image from '../core/Image'

class ArrowButton extends React.Component {
  render() {
    return (  
      <Button className='arrow' onClick={this.props.onClick} to={this.props.href}>
        {this.props.children}
        <Image src={arrowImage} height={10} width={10} />
      </Button>
    )
  }
}

export default ArrowButton;
