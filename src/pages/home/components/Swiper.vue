<template>
<div class="wrap">
  <swiper :options="swiperOption">
    <swiper-slide v-for='item of swiperList' :key='item.id'>
      <img class="swiper-img" :src="item.imgUrl"></swiper-slide>
    <div class="swiper-pagination btn"  slot="pagination"></div>
  </swiper>
</div>
</template>
<script>
export default{
  name: 'HomeSwiper',
  props: {
    swiperList: Array
  },
  data: function () {
    return {
      swiperOption: {
        pagination: '.swiper-pagination',
        loop: true
      }
    }
  }
}
</script>
<style lang='stylus' scoped>
.wrap >>> .swiper-pagination-bullet-active
  background: #fff !important
.wrap
  overflow: hidden
  width: 100%
  height: 0
  padding-bottom: 31.25%
  .swiper-img
    width:100%
</style>
