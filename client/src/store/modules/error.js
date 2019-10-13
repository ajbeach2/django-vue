import {
  SET_ERRORS,
  CLEAR_ERRORS
} from '../types'

const state = {
  items: {}
}

const getters = {
  error: state => state.items
}

const actions = {
  setErrors: ({ commit }, data) => {
    commit(SET_ERRORS, data)
  },
  clearErrors: ({ commit }) => {
    commit(CLEAR_ERRORS)
  }
}

const mutations = {
  [SET_ERRORS] (state, data) {
    state.items = Object.assign({}, data)
  },
  [CLEAR_ERRORS] (state, action) {
    state.items = {}
  }
}

export default {
  state,
  getters,
  actions,
  mutations
}
