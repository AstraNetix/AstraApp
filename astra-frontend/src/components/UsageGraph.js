import React from 'react'
import moment from 'moment'
import {Container} from 'flux/utils';
import { LineChart, Line, CartesianGrid, XAxis, YAxis, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import Button from './core/Button'
import CurrentDeviceStore from '../stores/CurrentDeviceStore'

import '../css/DeviceView.css'
import '../css/Button.css'

class UsageGraph extends React.Component {
  static getStores() {
    return [CurrentDeviceStore];
  }

  static calculateState(prevState) {
    let today = new Date();

    /* Do fine data */
    let fineDataRaw = CurrentDeviceStore.getFineData();
    var yesterday = new Date();
    yesterday.setDate(today.getDate() - 1);

    var fineData = []; 
    while (yesterday <= today) {
      fineData.push({time: yesterday.getTime()});
      yesterday.setTime(yesterday.getTime() + (5 * 60 * 1000));
    }

    fineData.forEach((dataPoint, i) => {  
      Object.keys(fineDataRaw).forEach((type) => {
        dataPoint[type] = fineDataRaw[type][i];
      });
    });

    /* Do coarse data */
    let coarseDataRaw = CurrentDeviceStore.getCoarseData();
    var aWhileAgo = new Date()
    aWhileAgo.setDate(today.getDate - 90);

    var coarseData = []; 
    while (aWhileAgo <= today) {
      coarseData.push({time: aWhileAgo.getTime()});
      aWhileAgo.setTime(aWhileAgo.getTime() + (24 * 60 * 60 * 1000));
    }

    coarseData.forEach((dataPoint, i) => {  
      Object.keys(coarseDataRaw).forEach((type) => {
        dataPoint[type] = coarseDataRaw[type][i];
      });
    });

    return {
      detail: prevState !== undefined ? prevState.detail : 'fine', 
      fineData: fineData, 
      coarseData: coarseData,
    };
  }

  showFine = () => { this.setState({detail: 'fine'}); }

  showCoarse = () => { this.setState({detail: 'coarse'}); }

  render() {
    return(
      <div className='usage-graph'>
        <div style={{position: 'absolute'}}>
          <Button handleClick={this.showFine} className='small-select' 
            style={{borderTopLeftRadius: '20px', borderBottomLeftRadius: '20px', 
            background: this.state.detail === 'fine' ? '#646464' : 'none', 
            color: this.state.detail === 'fine' ? '#dfdfdf' : '#646464', marginLeft: '1em'}}> 
            Day 
          </Button>
          <Button handleClick={this.showCoarse} className='small-select'
          style={{borderTopRightRadius: '20px', borderBottomRightRadius: '20px',
            background: this.state.detail === 'coarse' ? '#646464' : 'none', 
            color: this.state.detail === 'coarse' ? '#dfdfdf' : '#646464'}}> 
            3 months 
          </Button>
        </div>
        <ResponsiveContainer height={350} width='100%'>
          <LineChart 
            data={this.state.detail === 'fine' ? this.state.fineData : this.state.coarseData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis 
              dataKey='time' 
              name = 'Time' 
              domain={['dataMin', 'dataMax']}
              type = 'number'
              tickFormatter={(time) => {
                return this.state.detail === 'fine' ? moment(time).format('M/D h:mm') : moment(time).format('M');
              }}/>
            <YAxis tickFormatter={(percent) => percent + "%"} width={50}/>
            <Legend align='right' verticalAlign='top' iconType='circle' height={36}/>
            <Tooltip 
              wrapperStyle={{borderRadius: '5px'}}
              labelFormatter={(time) => {
                return this.state.detail === 'fine' ? moment(time).format('dddd hh:mmA') : moment(time).format('MMMM DD');
              }}/>
            <Line type="monotone" dataKey="cpu" stroke="#8884d8" dot={false}/>
            <Line type="monotone" dataKey="gpu" stroke="#82ca9d" dot={false}/>
            <Line type="monotone" dataKey="disk" stroke="#dab618" dot={false}/>
            <Line type="monotone" dataKey="network" stroke="#9f50b8" dot={false}/>
          </LineChart>
        </ResponsiveContainer>
      </div>
    );
  }
}

export default Container.create(UsageGraph);