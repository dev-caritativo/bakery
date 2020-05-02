import Vue from 'vue'
export const state = () => ({
  pastry: [],
  ingredients: [],
  pastry_ingredients: []
})

export const getters = {
  pastries: state => state.pastry,
  pastry: state => (params) => {
    return state.pastry.find(e => e.id === parseInt(params))
  },
  ingredients: state => state.ingredients,
  ingredient: state => (pi) => {
    return state.ingredients.find(e => e.id === parseInt(pi))
  },
  ingredient_names: (state) => {
    return state.ingredients.map((a) => {
      return {
        name: a.name,
        id: a.id
      }
    })
  },
  pastry_ingredients: state => (p) => {
    return state.pastry_ingredients.filter(e => e.pastry === parseInt(p))
  }
}

export const mutations = {
  AppendPastry (state, res) {
    state.pastry.push({
      id: res.id,
      name: res.name
    })
  },
  AppendPastries (state, data) {
    state.pastry = []
    data.forEach((res) => {
      state.pastry.push({
        id: res.id,
        name: res.name
      })
    })
  },
  UpdatePastry (state, obj) {
    state.pastry.forEach((e, index) => {
      if (e.id === obj.id) { Vue.set(state.pastry, index, obj) }
    })
  },
  AppendIngredients (state, data) {
    data.forEach((res) => {
      const ix = state.ingredients.map(a => a.name).indexOf(res.name)
      if (ix === -1) {
        state.ingredients.push(res)
      } else {
        Vue.set(state.ingredients, ix, res)
      }
    })
  },
  AppendPastryIngredients (state, { obj, data }) {
    data.forEach((res) => {
      const ix = state.pastry_ingredients.map(a => a.id).indexOf(res.id)
      if (ix === -1) {
        state.pastry_ingredients.push(res)
      } else {
        Vue.set(state.pastry_ingredients, ix, res)
      }
    })
  },
  AppendPastryIngredient (state, data) {
    const ix = state.pastry_ingredients.map(a => a.id).indexOf(data.id)
    if (ix === -1) {
      state.pastry_ingredients.push(data)
    } else {
      Vue.set(state.pastry_ingredients, ix, data)
    }
  },
  DeletePastryIngredient (state, data) {
    console.log(data)
    const ix = state.pastry_ingredients.map(a => a.id).indexOf(data.id)
    state.pastry_ingredients.splice(ix, 1)
  }
}

export const actions = {
  async GetPastries ({
    commit,
    $axios
  }, obj) {
    const data = await this.$axios
      .$get(process.env.API_URL + 'pastry/')
      .catch((error) => {
        if (error.response) {
          console.log(error.response)
          // this.errors = [error.response.data.message]
        } else {
          console.log('Error', error.message)
        }
      })
    await commit('AppendPastries', data)
  },
  async GetIngredients ({
    commit,
    $axios
  }, obj) {
    const data = await this.$axios
      .$get(process.env.API_URL + 'ingredients/')
      .catch((error) => {
        if (error.response) {
          console.log(error.response)
          // this.errors = [error.response.data.message]
        } else {
          console.log('Error', error.message)
        }
      })
    await commit('AppendIngredients', data)
  },
  async GetPastryIngredients ({
    commit,
    $axios
  }, obj) {
    const data = await this.$axios
      .$get(process.env.API_URL + 'pastry/ingredients', {
        params: {
          id: parseInt(obj)
        }
      })
      .catch((error) => {
        if (error.response) {
          console.log(error.response)
          // this.errors = [error.response.data.message]
        } else {
          console.log('Error', error.message)
        }
      })
    await commit('AppendPastryIngredients', { obj, data })
  },
  async AddPastryIngredients ({
    commit
  }, {
    id,
    val
  }) {
    const data = await this.$axios
      .$post(process.env.API_URL + 'pastry/ingredients', {
        iid: id,
        value: val
      })
      .catch((error) => {
        if (error.response) {
          console.log(error.response)
          // this.errors = [error.response.data.message]
        } else {
          console.log('Error', error.message)
        }
      })
    await commit('AppendPastryIngredient', data)
  },
  async UpdatePastryIngredients ({ commit }, {
    val,
    obj
  }) {
    const data = await this.$axios
      .$put(process.env.API_URL + 'pastry/ingredients', {
        id: obj,
        value: val
      })
      .catch((error) => {
        if (error.response) {
          console.log(error.response)
          // this.errors = [error.response.data.message]
        } else {
          console.log('Error', error.message)
        }
      })
    await commit('AppendPastryIngredient', data)
  },
  async DeletePastryIngredients ({ commit }, {
    obj
  }) {
    const data = await this.$axios
      .$delete(process.env.API_URL + 'pastry/ingredients', {
        data: {
          iid: obj
        }
      })
      .catch((error) => {
        if (error.response) {
          console.log(error.response)
          // this.errors = [error.response.data.message]
        } else {
          console.log('Error', error.message)
        }
      })
    await commit('DeletePastryIngredient', data)
  }
}
