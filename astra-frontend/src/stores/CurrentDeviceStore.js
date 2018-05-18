import ActionConstants from '../constants/ActionConstants'
import Dispatcher from '../dispatcher'
import ServerAPI from '../ServerAPI'
import {Store} from 'flux/utils'

class CurrentDeviceStore extends Store {
  constructor(dispatcher) {
    super(dispatcher);
    this.uid = 2;
    this.info = {
      name: "Soham's Macbook Pro",
      model: 'Apple Macbook Pro',
      processor: '2Ghz Intel Core I7',
      graphics: 'Intel Iris Graphics 570',
      memory: '8GB 1867 MHz LPDDR3',
      type: 'laptop',
    };
    this.projects = {}; // {url: [name, status]}
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
    /* Holds data for past 24 hours, 1 point for every 5 min, each point 3 digits in length */
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
    
    for (var i = 0; i < 288; i++) {
      this.fineData.cpu.push(Math.floor(0.0002*Math.pow(i, 3) + 50*Math.random()));
      this.fineData.gpu.push(Math.floor(100*Math.exp(-i)*Math.abs(Math.cos(i/5)) + 10*Math.random()));
      this.fineData.disk.push(Math.floor(0.04*Math.pow(i - 48, 2) + 20*Math.random()));
      this.fineData.network.push(Math.floor((0.00000004*Math.pow(i, 4) + 0.03*Math.pow(i, 2) + 0.4*i) + 50*Math.random()));
    }
  }

  getUID() { return this.uid; }

  getInfo() { return this.info; }

  getProjects() { return this.projects; }

  getPreferences() { return this.preferences; }

  getLimits() { return this.limits; }

  getTimes() { return this.times; }
  
  getFineData() { return this.fineData; }

  getCoarseData() { return this.CoarseData; }

  __onDispatch(action) {
    var storeData;
    switch(action.type) {
      case ActionConstants.LOGIN:
        if (action.response.status !== 200) { break; } 
        this.uid = action.response.uid;
        storeData = ServerAPI.getDeviceStore(action.response.uid);

        this.info = storeData.info;
        this.projects = storeData.projects;
        this.preferences = storeData.preferences;
        this.limits = storeData.limits;
        this.times = storeData.times;
        this.coarseData = storeData.coarseData;
        this.fineData = storeData.fineData;
        
        break;
      case ActionConstants.DEVICE_CHANGE:
        storeData = action.response;

        this.info = storeData.info;
        this.projects = storeData.projects;
        this.preferences = storeData.preferences;
        this.limits = storeData.limits;
        this.times = storeData.times;
        this.coarseData = storeData.coarseData;
        this.fineData = storeData.fineData;

        break
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