<template>
<div>
   <home-header></home-header>
   <home-swiper></home-swiper>
   <home-icons></home-icons>
   <home-recommend></home-recommend>
   <home-weekend></home-weekend>
</div>
</template>

<script>
import HomeHeader from '@/pages/home/components/Header.vue'
import HomeSwiper from '@/pages/home/components/Swiper.vue'
import HomeIcons from '@/pages/home/components/Icons.vue'
import HomeRecommend from '@/pages/home/components/Recommend.vue'
import HomeWeekend from '@/pages/home/components/Weekend.vue'
export default {
  name: 'Home',
  components: {
    HomeHeader,
    HomeSwiper,
    HomeIcons,
    HomeRecommend,
    HomeWeekend
  }
}
</script>

<style>

</style>
