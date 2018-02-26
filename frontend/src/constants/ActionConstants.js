import ServerAPI from '../ServerAPI'

export default {
  BOOTSTRAP: {method: null, value: 'BOOTSTRAP'},
  LOGIN: {method: ServerAPI.loginUser, value: 'LOGIN'},
  LOGOUT: {method: ServerAPI.logoutUser, value: 'LOGOUT'},
  ADD_PROJECT: {method: ServerAPI.addProject, value: 'ADD_PROJECT'},
  REMOVE_PROJECT: {method: ServerAPI.removeProject, value: 'REMOVE_PROJECT'},
};