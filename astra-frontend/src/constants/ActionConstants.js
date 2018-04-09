import ServerAPI from '../ServerAPI'

export default {
  REGISTER: {method: ServerAPI.createUser, value: 'REGISTER'},
  BOOTSTRAP: {method: null, value: 'BOOTSTRAP'},
  LOGIN: {method: ServerAPI.loginUser, value: 'LOGIN'},
  LOGOUT: {method: ServerAPI.logoutUser, value: 'LOGOUT'},
  START_PROJECT: {method: ServerAPI.addProject, value: 'ADD_PROJECT'},
  END_PROJECT: {method: ServerAPI.removeProject, value: 'REMOVE_PROJECT'},
};