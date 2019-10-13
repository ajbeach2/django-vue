import axios from 'axios'
import Cookies from 'js-cookie'
import router from '@/router'
import store from '@/store'

const API_URL = process.env.API_ROOT || 'http://localhost:8000/api'

axios.interceptors.request.use(function (config) {
  var csrftoken = Cookies.get('csrftoken')
  config.headers = config.headers || {}
  config.withCredentials = true
  if (csrftoken) {
    config.headers['X-CSRFToken'] = csrftoken
  }
  return config
}, function (error) {
  return Promise.reject(error)
})

axios.interceptors.response.use(function (response) {
  return response
}, function (error) {
  return Promise.reject(error)
})

export default {
  login (data) {
    const url = `${API_URL}/login/`
    return axios.post(url, data)
  },
  register (data) {
    const url = `${API_URL}/register/`
    return axios.post(url, data)
  },
  logout (data) {
    const url = `${API_URL}/logout/`
    return axios.post(url, data)
  },
  getMe (data) {
    const url = `${API_URL}/login/`
    return axios.get(url)
  }
}
