require('whatwg-fetch');

const React = require('react');
const Cookie = require('js-cookie');

const apiHead = "api"
const emailCookie = Cookie.get('email')

export default class ServerAPI extends React.Component {
  getUser(email) {
    return _get("users/is/", {'email': email})
  }

  loginUser(email, password) {
    return _post("users/basic/login_user/", {'email': email, 'password': password})
  }

  logoutUser() {
    return _delete("users/id/logout_user/")
  }

  setUserVerified() {
    return _patch("users/id/set_user_verified/", {'email': emailCookie})
  }

  isUserValidForSale() {
    return _get("users/id/user_valid_for_sale", {'email': emailCookie})
  }

  createUser(name, email, password, confirmPassword) {
    return _post("users/basic/", {'name': name, 'email': email, 
      'password': password, 'confirm_password': confirmPassword})
  }

  deleteUser() {
    return _delete("users/id", {'email': emailCookie})
  }

  resetUserPassword(email, newPassword) {
    return _patch("users/password/reset_password/", {'email': email, 'new_password': newPassword})
  }

  changeUserPassword(oldPassword, newPassword) {
    return _patch("users/password/change_password/", {'email': emailCookie, 'old_password': oldPassword, 'new_password': newPassword})
  }

  getUserDevices() {
    return _patch("users/id/devices", {'email': emailCookie})
  }

  getDeviceInfo(deviceID) {
    return _patch("devices/id/info", {'email': emailCookie, 'device_id': deviceID})
  }

  getDeviceProjects(deviceID) {
    return _patch("devices/id/projects", {'email': emailCookie, 'device_id': deviceID})
  }

  startProject(url, deviceID) {
    return _patch("users/relational/start_project", {'email': emailCookie, 'device_id': deviceID, 'url': url})
  }

  stopProject(url, deviceID) {
    return _patch("users/relational/stop_project", {'email': emailCookie, 'device_id': deviceID, 'url': url})
  }

  stopProject(url, deviceID) {
    return _patch("users/relational/suspend_project", {'email': emailCookie, 'device_id': deviceID, 'url': url})
  }

  changeUsageTimes(deviceID, days, startTime, endTime) {
    return _patch("devices/usage/change_usage_times", {'email': emailCookie, 'device_id': deviceID,
    'days': days, 'start_time': startTime, 'end_time': endTime})
  }

  changeCPUPercent(deviceID, percent) {
    return _patch("devices/usage/cpu_percent", {'email': emailCookie, 'device_id': deviceID,
    'percent': percent})
  }

  changeCPUCores(deviceID, numCores) {
    return _patch("devices/usage/cpu_percent", {'email': emailCookie, 'device_id': deviceID,
    'num_cores': numCores})
  }

  changeDiskPercent(deviceID, percent) {
    return _patch("devices/usage/disk_percent", {'email': emailCookie, 'device_id': deviceID,
    'percent': percent})
  }

  changeRAMPercent(deviceID, percent) {
    return _patch("devices/usage/ram_percent", {'email': emailCookie, 'device_id': deviceID,
    'percent': percent})
  }

  changeNetworkDown(deviceID, kbps) {
    return _patch("devices/usage/network_down", {'email': emailCookie, 'device_id': deviceID,
    'kbps': kbps})
  }

  runOnBatteries(deviceID, value) {
    return _patch("devices/preferences/run_on_batteries", {'email': emailCookie, 'device_id': deviceID,
    'value': value})
  }

  runifInactive(deviceID, value) {
    return _patch("devices/preferences/run_if_inactive", {'email': emailCookie, 'device_id': deviceID,
    'value': value})
  }

  useMemoryOnly(deviceID, value) {
    return _patch("devices/preferences/use_memory_only", {'email': emailCookie, 'device_id': deviceID,
    'value': value})
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


