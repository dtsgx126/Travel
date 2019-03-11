<template>
<div>
  <city-header></city-header>
  <city-search></city-search>
  <city-list></city-list>
  <city-alphabet></city-alphabet>
</div>
</template>
<script>
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
  }
}
</script>
<style lang='stylus' scoped>

</style>
