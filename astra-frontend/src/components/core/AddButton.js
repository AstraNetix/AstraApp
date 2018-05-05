import React from 'react'
import Button from './Button'
import Image from './Image'
import addImage from '../../images/Add.png'
import addWhiteImage from '../../images/Addwhite.png'
import '../../css/Button.css'

class AddButton extends React.Component {
  constructor(props) {
    super(props);
    let {type, height, width, ...extraProps} = this.props;

    this.state = {
      type: type || 'rectangular',
      height: height || 15,
      width: width || 15,
      image: addImage,
    };
  }

  _mouseEnter = () => {
    this.setState({image: addWhiteImage})
  }

  _mouseLeave = () => {
    this.setState({image: addImage})
  }

  render() {
    let style = {padding: this.state.type === 'rectangular' ? '5px 20px' : '5px 6px'};
    return (
      <Button className='add-button' onMouseEnter={this._mouseEnter} onMouseLeave={this._mouseLeave}
        onClick={this.props.onClick} style={style}> 
        <Image src={this.state.image} height={this.state.height} width={this.state.width}/>
      </Button>
    );
  }
}

export default AddButton;