require('whatwg-fetch');

const React = require('react');
const Cookie = require('js-cookie');

const apiHead = "api"
const emailCookie = Cookie.get('email')

export default class ServerAPI extends React.Component {
  getUser(email) {
    return _get("users/is/", {email: email})
  }

  loginUser(email, password) {
    return _post("users/basic/login_user/", {email: email, password: password})
  }

  logoutUser() {
    return _delete("users/id/logout_user/")
  }

  setUserVerified() {
    return _patch("users/id/set_user_verified/", {email: emailCookie})
  }

  isUserValidForSale() {
    return _get("users/id/user_valid_for_sale", {email: emailCookie})
  }

  createUser(email, password, firstName, lastName) {
    return _post("users/basic/", {email: email, password: password, 
      first_name: firstName, last_name: lastName})
  }

  deleteUser() {
    return _delete("users/id", {email: emailCookie})
  }

  resetUserPassword(email, newPassword) {
    return _patch("password/reset_password/", {email: email, new_password: newPassword})
  }

  changeUserPassword(email, oldPassword, newPassword) {
    return _patch("password/change_password/", {email: email, old_password: oldPassword, new_password: newPassword})
  }

  addProject(projectID, deviceID) {
    return _patch("users/relational/start_project", {email: emailCookie, device_id: deviceID, 'project-id': projectID})
  }

  removeProject(projectID, deviceID) {
    return _patch("users/relational/stop_project", {email: emailCookie, device_id: deviceID, project_id: projectID})
  }

}

function _ajax(method, uri, data) {
  const isSafeMethod = /^(GET|HEAD|OPTIONS|TRACE)$/.test(method);
  const params = {
    method: method,
    credentials: 'same-origin',
    headers: {
      'Content-Type': 'application/json',
    },
  };
  if (!isSafeMethod) {
    params.headers['X-CSRFToken'] = Cookie.get('csrftoken');
    if (data) {
      params.body = typeof data === 'string' ? data : JSON.stringify(data);
    }
  }

  return fetch(apiHead + uri, params).then(response =>
    response.ok ? 
      response.json() :
      response.json().then(json => Promise.reject(json)),
  ).catch(error => { 
      throw Error(error.message) 
    }
  ); 
}

const _delete = _ajax.bind(null, 'DELETE');
const _get = _ajax.bind(null, 'GET');
const _patch = _ajax.bind(null, 'PATCH');
const _put = _ajax.bind(null, 'PUT');
const _post = _ajax.bind(null, 'POST');


