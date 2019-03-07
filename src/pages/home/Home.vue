
<template>
<div>
   <home-header></home-header>
   <home-swiper></home-swiper>
   <home-icons></home-icons>
</div>
</template>

<script>
import HomeHeader from '@/pages/home/components/Header.vue'
import HomeSwiper from '@/pages/home/components/Swiper.vue'
import HomeIcons from '@/pages/home/components/Icons.vue'
export default {
  name: 'Home',
  components: {
    HomeHeader,
    HomeSwiper,
    HomeIcons
  }

}
</script>

<style>

</style>
