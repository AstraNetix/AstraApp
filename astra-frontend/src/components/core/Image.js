import React, {Component} from 'react';
import '../../css/Image.css'

export default class Image extends Component {  
  render() {
    let {mode, src, height, width, shape, style, ...props} = this.props;
    let modes = {
      'fill': 'cover',
      'fit': 'contain'
    };
    let size = modes[mode] || 'contain';

    let defaults = {
      height: height || 100,
      width: width || 100,
      shape: shape || 'rectangular',
      backgroundColor: 'none',
      borderColor: 'none',
    };

    let important = {
      backgroundImage: `url("${src}")`,
      backgroundSize: 'cover',
      backgroundPosition: 'center center',
      backgroundRepeat: 'no-repeat'
    };

    return <div {...props} style={{...defaults, ...style, ...important}} />
  }
}