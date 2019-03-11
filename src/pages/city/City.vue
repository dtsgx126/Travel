<template>
<div>
  <city-header></city-header>
  <city-search></city-search>
  <city-list></city-list>
</div>
</template>
<script>
import CityHeader from '@/pages/city/header/Header'
import CitySearch from '@/pages/city/search/Search'
import CityList from '@/pages/city/citylist/CityList'
export default{
  name: 'City',
  components: {
    CityHeader,
    CitySearch,
    CityList
  }
}
</script>
<style lang='stylus' scoped>

</style>
