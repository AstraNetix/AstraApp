import ActionConstants from '../constants/ActionConstants'
import DeviceConstants from '../constants/DeviceConstants'
import Dispatcher from '../dispatcher'
import {Store} from 'flux/utils'

class ProjectsStore extends Store {
  constructor(dispatcher) {
    super(dispatcher);
    this.areas = [
      'Physics',
      'Mathematics',
      'Astrophysics',
      'Computer Science',
      'Climate study',
      'Astronomy',
      'Cryptography',
      'Molecular Biology',
      'Chemistry',
      'Cognitive Science',
      'Seismology',
      'Environmental',
      'Medical',
    ]
    this.projects = {
      'https://einsteinathome.org/': {
        name: 'Einstein@home',
        sponsors: [
          'University of Wisconsin - Milwaukee (USA)', 
          'Max Planck Institute for Gravitational Physics - Hanover (Germany)'
        ],
        contributors: 400,
        blurb: "Einstein@Home uses your computer's idle time to search for weak astrophysical signals from spinning neutron stars (often called pulsars) using data from the LIGO gravitational-wave detectors, the Arecibo radio telescope, and the Fermi gamma-ray satellite.", 
        description: "Einstein@Home is a World Year of Physics 2005 and an International Year of Astronomy 2009 project. It is supported by the American Physical Society (APS), the US National Science Foundation (NSF), the Max Planck Society (MPG), and a number of international organizations.\nEinstein@Home uses your computer's idle time to search for weak astrophysical signals from spinning neutron stars (often called pulsars) using data from the LIGO gravitational-wave detectors, the Arecibo radio telescope, and the Fermi gamma-ray satellite. Einstein@Home volunteers have already discovered about fifty new neutron stars, and we hope to find many more.\nOur long-term goal is to make the first direct detections of gravitational-wave emission from spinning neutron stars. Gravitational waves were predicted by Albert Einstein a century ago, and were directly seen for the first time on September 14, 2015. This observation of gravitational waves from a pair of merging black holes opens up a new window on the universe, and ushers in a new era in astronomy.\nThis first direct measurement was made soon after the advanced LIGO instruments came online after an extensive five-year upgrade. These advanced detectors took data between September 2015 and January 2016 and can already \"see\" three to six times as far as initial LIGO, depending upon the source type. Over the next two years this will increase to a factor of ten or more, increasing the number of potentially-visible gravitational-wave sources by a factor of a thousand!",
        area: 'Astronomy',
        color: [55, 85, 185],
        platforms: [DeviceConstants.WINDOWS, DeviceConstants.MACOS, DeviceConstants.LINUX],
        isRunning: false,
      },
    } ;// {url: {name, sponsors, description, area, platforms, isRunning}}
  }

  getAreas() {
    return this.areas;
  }

  getProjects() {
    return this.projects;
  }

  getProject(url) {
    return this.projects[url];
  }

  __onDispatch(action) {
    switch(action.type) {
      case ActionConstants.GET_PROJECTS:
        action.response.data;
    };
    this.__emitChange();
  }
}

export default new ProjectsStore(Dispatcher);