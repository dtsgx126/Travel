<template>
<div>
  <city-header></city-header>
  <city-search></city-search>
  <city-list :cities='cities' :hot='hotCities'></city-list>
  <city-alphabet :cities='cities'></city-alphabet>
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
      hotCities: []
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
        // console.log(this.cities)
      }
    }
  },
  mounted: function () {
    this.getCityInfo()
  }
}
</script>
<style lang='stylus' scoped>

</style>
