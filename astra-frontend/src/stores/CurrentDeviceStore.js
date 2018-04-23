'use strict'

import ActionConstants from '../constants/ActionConstants'
import Dispatcher from '../dispatcher'
import ServerAPI from '../ServerAPI'
import {Store} from 'flux/utils'

class CurrentDeviceStore extends Store {
  constructor(dispatcher) {
    super(dispatcher);
    this.uid = 0;
    this.info = {
      name: '',
      models: '',
      processor: '',
      graphics: '',
      memory: '',
      type: '',
    };
    this.projects = {};
    this.preferences= {
      runOnBatteries: false,
      runIfActive: false,
      useMemoryOnly: false,
    };
    this.limits = {
      cpu: {usage: 50, cores: 1},
      disk: {usage: 50},
      ram: {usage: 50},
      network: {downByte: 0, upBytes: 0},
    };
    this.times = {
      monday: {start: 0, end: 24},
      tuesday: {start: 0, end: 24},
      wednesday: {start: 0, end: 24},
      thursday: {start: 0, end: 24},
      friday: {start: 0, end: 24},
      saturday: {start: 0, end: 24},
      sunday: {start: 0, end: 24},
    };
    /* Holds data for past 24 hours, 1 point for every 30 min, each point 3 digits in length */
    this.fineData = {
      cpu: [], 
      gpu: [], 
      disk: [], 
      network: [], 
    };
    /* Holds data for the past 90 days, 1 point for every day, each point 3 digits in length */
    this.coarseData = {
      cpu: [], 
      gpu: [], 
      disk: [], 
      network: [], 
    }; 
  }

  getInfo() { return this.state.info; }

  getProjects() { return this.state.projects; }

  getPreferences() { return this.state.preferences; }

  getLimits() { return this.state.limits; }

  getTimes() { return this.state.times; }

  __onDispatch(action) {{ return; }
    switch(action.type) {
      case ActionConstant.LOGIN:
        if (action.response.status !== 200) { break; } 

        const deviceInfo = ServerAPI.getDeviceInfo(this.uid);
        this.info = deviceInfo.data.info;
        this.preferences = deviceInfo.data.preferences;
        this.limits = deviceInfo.data.limits;
        this.times = deviceInfo.data.times;

        this.projects = ServerAPI.getDeviceProjects(this.uid).data;

        const deviceData = ServerAPI.getDeviceData(this.uid);
        this.fineData = deviceData.data.fineData;
        this.coarseData = deviceData.data.coarseData;
        
        break;
      case ActionConstants.LOGOUT:
        this._currentDevice = {};
        break;  
      default:
        return;
    }

    this.__emitChange();
  }
}

export default new CurrentDeviceStore(Dispatcher);