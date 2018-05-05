require('whatwg-fetch');
const Cookie = require('js-cookie');

const API = 'http://127.0.0.1:8000/api';
const emailCookie = Cookie.get('email')

class ServerAPI {
  login(email, password) {
    return _patch("users/basic/login_user/", {'email': email, 'password': password})
  }

  logout() {
    return _patch("users/id/logout_user/")
  }

  setUserVerified() {
    return _patch("users/id/set_user_verified/", {'email': emailCookie})
  }

  isUserValidForSale() {
    return _patch("users/id/user_valid_for_sale", {'email': emailCookie})
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
    return _patch("users/id/get_devices", {'email': emailCookie})
  }

  getDeviceStore(deviceID) {
    return _patch("devices/id/store_data", {'email': emailCookie, 'device_id': deviceID})
  }

  getDeviceInfo(deviceID) {
    return _patch("devices/id/info", {'email': emailCookie, 'device_id': deviceID})
  }

  getDeviceData(deviceID) {
    return _patch("devices/id/data", {'email': emailCookie, 'device_id': deviceID})
  }

  getDeviceProjects(deviceID) {
    return _patch("devices/id/projects", {'email': emailCookie, 'device_id': deviceID})
  }

  startProject(url, deviceID) {
    return _patch("users/relational/start_project", {'email': emailCookie, 'device_id': deviceID, 'url': url})
  }

  quitProject(url, deviceID) {
    return _patch("users/relational/quit_project", {'email': emailCookie, 'device_id': deviceID, 'url': url})
  }

  suspendProject(url, deviceID) {
    return _patch("users/relational/suspend_project", {'email': emailCookie, 'device_id': deviceID, 'url': url})
  }

  changeUsageTimes(deviceID, days, startTime, endTime) {
    return _patch("devices/usage/config_hours", {'email': emailCookie, 'device_id': deviceID,
    'days': days, 'start_time': startTime, 'end_time': endTime})
  }

  changeCPUPercent(deviceID, percent) {
    return _patch("devices/usage/cpu_percent", {'email': emailCookie, 'device_id': deviceID,
    'percent': percent})
  }

  changeCPUCores(deviceID, numCores) {
    return _patch("devices/usage/max_cpus", {'email': emailCookie, 'device_id': deviceID,
    'max_cpus': numCores})
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

  changeNetworkUp(deviceID, kbps) {
    return _patch("devices/usage/network_up", {'email': emailCookie, 'device_id': deviceID,
    'kbps': kbps})
  }

  runOnBatteries(deviceID, value) {
    return _patch("devices/preferences/run_on_batteries", {'email': emailCookie, 'device_id': deviceID,
    'value': value})
  }

  runIfActive(deviceID, value) {
    return _patch("devices/preferences/run_if_active", {'email': emailCookie, 'device_id': deviceID,
    'value': value})
  }

  useMemoryOnly(deviceID, value) {
    return _patch("devices/preferences/use_memory_only", {'email': emailCookie, 'device_id': deviceID,
    'value': value})
  }

}

function _ajax(method, uri, data, content_type) {
  if (content_type == null) {
    content_type = 'application/json';
  }

  const params = {
    method: method,
    credentials: 'same-origin',
    headers: {
      'Authorization': 'Basic ' + window.btoa('apimaster@gmail.com:Api1@useR'),
      'Content-Type': content_type,
    },
  };

  if (data && content_type !== 'multipart/form-data') {
    params.body = typeof data === 'string' ? data : JSON.stringify(data);
  } else if (data && content_type === 'multipart/form-data') {
    var form = new FormData();
    form.append('file', data['file']);
    params.body = form;
  }

  if (content_type === 'application/json') {
    return fetch(API + uri, params).then(response =>
      response.ok ? 
        response.json() :
        response.json().then(json => Promise.reject(json)),
    ).catch(error => { 
      throw Error(error.message) 
    }); 
  } else if (content_type === 'application/force-download') {
    return fetch(uri, params).then(
      response =>
        response.ok
          ? response.blob()
          : response.blob().then(json => Promise.reject(json)),
    );
  } else {
    return fetch(uri, params).then(
      response =>
        response.ok
          ? response.text()
          : response.text().then(text => Promise.reject(text)),
    );
  }
}

const _delete = _ajax.bind(null, 'DELETE');
const _get = _ajax.bind(null, 'GET');
const _patch = _ajax.bind(null, 'PATCH');
const _put = _ajax.bind(null, 'PUT');
const _post = _ajax.bind(null, 'POST');

export default ServerAPI;