<template>
<div>
   <home-header :city="city"></home-header>
   <home-swiper :swiperList="swiperList"></home-swiper>
   <home-icons :iconList='iconList'></home-icons>
   <home-recommend :recommendList='recommendList'></home-recommend>
   <home-weekend :weekendList='weekendList'></home-weekend>
</div>
</template>

<script>
import HomeHeader from '@/pages/home/components/Header.vue'
import HomeSwiper from '@/pages/home/components/Swiper.vue'
import HomeIcons from '@/pages/home/components/Icons.vue'
import HomeRecommend from '@/pages/home/components/Recommend.vue'
import HomeWeekend from '@/pages/home/components/Weekend.vue'
import axios from 'axios'
export default {
  name: 'Home',
  components: {
    HomeHeader,
    HomeSwiper,
    HomeIcons,
    HomeRecommend,
    HomeWeekend
  },
  data: function () {
    return {
      city: '',
      iconList: [],
      recommendList: [],
      swiperList: [],
      weekendList: []
    }
  },
  methods: {
    getHomeInfo () {
      axios.get('/api/index.json')
        .then(this.getHomeInfoSucc)
    },
    getHomeInfoSucc (res) {
      var data = res.data.data
      if (res.data.ret && data) {
        this.city = data.city
        this.iconList = data.iconList
        this.recommendList = data.recommendList
        this.swiperList = data.swiperList
        this.weekendList = data.weekendList
      }
    }
  },
  mounted () {
    this.getHomeInfo()
  }
}
</script>

<style>

</style>
