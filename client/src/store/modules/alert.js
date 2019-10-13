import {
  SHOW_ALERT,
  HIDE_ALERT
} from '../types'

const state = {
  items: []
}

const getters = {
  alerts: state => state.items
}

const actions = {
  showAlert: ({ commit }, data, delay = 30000) => {
    commit(SHOW_ALERT, data)
    setTimeout(() => {
      commit(HIDE_ALERT, data)
    }, delay)
  },
  hideAlert: ({ commit }, data) => {
    commit(HIDE_ALERT, data)
  }
}

const mutations = {
  [SHOW_ALERT] (state, data) {
    data.id = Date.now()
    state.items.push(data)
  },
  [HIDE_ALERT] (state, item) {
    let index = state.items.indexOf(item)
    if (index >= 0) {
      state.items.splice(index, 1)
    }
  }
}

export default {
  state,
  getters,
  actions,
  mutations
}
