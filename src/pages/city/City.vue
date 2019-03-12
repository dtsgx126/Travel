<template>
<div>
  <city-header></city-header>
  <city-search :cities='cities'></city-search>
  <city-list :cities='cities' :hot='hotCities' :letter='letter'></city-list>
  <city-alphabet :cities='cities' v-on:change='handleLetterChange'></city-alphabet>
</div>
</template>
<script>
import axios from 'axios'
import CityHeader from '@/pages/city/components/Header'
import CitySearch from '@/pages/city/components/Search'
import CityList from '@/pages/city/components/CityList'
import CityAlphabet from '@/pages/city/components/Alphabet'
export default{
  name: 'City',
  components: {
    CityHeader,
    CitySearch,
    CityList,
    CityAlphabet
  },
  data: function () {
    return {
      cities: {},
      hotCities: [],
      letter: ''
    }
  },
  methods: {
    getCityInfo: function () {
      axios.get('/api/city.json')
        .then(this.getCityInfoSuc)
    },
    getCityInfoSuc: function (res) {
      res = res.data
      if (res.ret && res.data) {
        res = res.data
        this.cities = res.cities
        this.hotCities = res.hotCities
      }
    },
    handleLetterChange: function (letter) {
      this.letter = letter
    }
  },
  mounted: function () {
    this.getCityInfo()
  }
}
</script>
<style lang='stylus' scoped>

</style>
