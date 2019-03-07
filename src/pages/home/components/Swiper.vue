<template>
<div class="wrap">
  <swiper :options="swiperOption">
    <swiper-slide v-for='item of swiperList'>
      <img class="swiper-img" :src="item.imgUrl" :key='item.id'></swiper-slide>
    <div class="swiper-pagination btn"  slot="pagination"></div>
  </swiper>
  <div>test</div>
</div>
</template>
<script>
export default{
  name: 'HomeSwiper',
  data: function () {
    return {
      swiperOption: {
      	pagination: '.swiper-pagination',
        loop: true
      },
      swiperList: [{
      	id: '0001',
      	imgUrl: 'http://mp-piao-admincp.qunarzz.com/mp_piao_admin_mp_piao_admin/admin/20192/6ad4363486f1fd6ff159f122bd838acd.jpg_750x200_dc715f94.jpg'
      },{
      	id: '0002',
      	imgUrl: 'http://mp-piao-admincp.qunarzz.com/mp_piao_admin_mp_piao_admin/admin/20193/700528b360c39d630dda13930a92a1a6.jpg_750x200_80f6150c.jpg'
      }]
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
  padding-bottom: 26.666667%
  .swiper-img
    width:100%
</style>
