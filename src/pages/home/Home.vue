<template>
<div>
   <home-header></home-header>
   <home-swiper></home-swiper>
   <home-icons></home-icons>
   <home-recommend></home-recommend>
</div>
</template>

<script>
import HomeHeader from '@/pages/home/components/Header.vue'
import HomeSwiper from '@/pages/home/components/Swiper.vue'
import HomeIcons from '@/pages/home/components/Icons.vue'
import HomeRecommend from '@/pages/home/components/Recommend.vue'
export default {
  name: 'Home',
  components: {
    HomeHeader,
    HomeSwiper,
    HomeIcons,
    HomeRecommend
  }
}
</script>

<style>

</style>
