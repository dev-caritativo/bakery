<template>
  <div class="container-fluid">
    <div class="col">
      <div class="row">
        <h1>{{ pastry.name }}</h1>
        <b-form inline>
          <Dropdown
            :options="ingredient_names"
            v-on:selected="ingredientSelect"
            v-on:filter="ingredientQuery"
            :disabled="false"
            :maxItem="10"
            name="ingredient"
            placeholder="Please select an option"
          />

          <b-button variant="primary" @click="addIngredient">
            Add +
          </b-button>
        </b-form>
      </div>
      <div class="row">
        {{ ingredients }}
        </div>
      <div class="row ingr-container">
        {{ pastry_ingredients }}
        <div v-for="(ingr, index) in pastry_ingredients">
          <h5>{{ get_ingredient(ingr).name }}</h5>
          <div>{{ get_ingredient(ingr).price }}</div>
          <div>
            <b-form inline>
              <label
              label="Amount"
              :label-for="`iamount${index}`">Amount: </label>
              <b-form-input
                :id="`iamount${index}`"
                class="mb-2 mr-sm-2 mb-sm-0"
                type="number"
                :value="ingr.unit"
                min="1"
                step="1"
                @change="ingredientGram($event, ingr)" /></b-form>
            </div>
          <b-button
            variant="danger"
            @click="deleteIngredient(ingr)">Delete</b-button>

          <div>{{ SumIngredient(ingr) }}</div>
          </div>
      </div>
      <div class="row">
        <div>Total Grams:{{ totalGrams }}</div>
        <div>
          <b-form inline>
              <label
              label="Amount"/>
              <b-form-input
                id="gpp"
                class="mb-2 mr-sm-2 mb-sm-0"
                type="number"
                :value="grams_per_piece"
                min="1"
                step="1"
                @change="total" /></b-form>
        </div>
        <div>Output in pcs: {{ OutputInPiece }}</div>
        <div>Total Cost: {{ totalCost.toFixed(2) }}</div>
        <div>Cost/pc: {{ (totalCost / grams_per_piece).toFixed(2) }}</div>
      </div>
    </div>

  </div>
</template>

<script>
import Dropdown from '@/components/Dropdown'
import { mapState, mapGetters } from 'vuex'

export default {
  async middleware ({ route, store }) {
    await store.dispatch('pastry/GetPastries')
    await store.dispatch('pastry/GetIngredients')
    await store.dispatch('pastry/GetPastryIngredients', route.params.id)
  },
  components: { Dropdown },
  data () {
    return {
      select_ingredient: null,
      total_grams: 0,
      grams_per_piece: 1
    }
  },
  computed: {
    pastry ({ $store, $route }) {
      return $store.getters['pastry/pastry']($route.params.id)
    },
    pastry_ingredients ({ $store, $route }) {
      return $store.getters['pastry/pastry_ingredients']($route.params.id)
    },
    totalGrams ({ $store, $route }) {
      return $store.state.pastry.pastry_ingredients.filter(e => e.pastry === parseInt($route.params.id)).reduce((a, b) => +a + +b.unit, 0)
    },
    OutputInPiece ({ $store, $route }) {
      const sum = $store.state.pastry.pastry_ingredients.filter(e => e.pastry === parseInt($route.params.id)).reduce((a, b) => +a + +b.unit, 0)
      return parseInt(parseFloat(sum) / parseFloat(this.grams_per_piece))
    },
    totalCost ({ $store, $route }) {
      function getCost (p) {
        return parseFloat($store.state.pastry.ingredients.find(e => e.id === parseInt(p)).price)
      }
      const indgr = $store.state.pastry.pastry_ingredients.filter(e => e.pastry === parseInt($route.params.id))
      const units = indgr.map(a => a.unit / 1000)
      const cost = indgr.map(a => a.ingredient).map(res => getCost(res))
      const total = [...units].map((e, i) => e * cost[i])
      return total.reduce((a, b) => a + b, 0)
    },
    ...mapState('pastry', {
      ingredients: 'ingredients'
    }),
    ...mapGetters('pastry', {
      ingredient_names: 'ingredient_names'
    })
  },
  methods: {
    ingredientSelect ($a) {
      this.select_ingredient = $a
    },
    async ingredientQuery ($a) {
      await this.$store.dispatch('pastry/GetIngredients')
    },
    addIngredient () {
      this.$store.dispatch('pastry/AddPastryIngredients',
        { id: this.$route.params.id, val: this.select_ingredient })
    },
    deleteIngredient (val) {
      this.$store.dispatch('pastry/DeletePastryIngredients',
        { obj: val })
    },
    get_ingredient (ingr) {
      return this.$store.getters['pastry/ingredient'](ingr.ingredient)
    },
    SumIngredient (obj) {
      const price = this.$store.getters['pastry/ingredient'](obj.ingredient).price
      return ((parseFloat(obj.unit) / 1000) * parseFloat(price)).toFixed(2)
    },
    ingredientGram (val, obj) {
      try {
        this.$store.dispatch('pastry/UpdatePastryIngredients', { val, obj })
      } catch (error) {
        console.log(error)
      }
    },
    total (val) {
      this.grams_per_piece = parseFloat(val)
    }
  }
}
</script>

<style>
.ingr-container{
  flex-direction: column;
}

.ingr-container > div{
  display: flex;
  justify-content: space-between;
}
</style>
