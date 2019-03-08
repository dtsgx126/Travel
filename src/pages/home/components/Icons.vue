<template>
  <div class="icons">
    <swiper :options="swiperOption">
        <swiper-slide v-for='(page,index) of pages' :key='index'>
            <div class="icon" v-for='item of page' :key='item.id'>
              <div class="icon-img">
              <img class="icon-img-content" :src="item.imgUrl">
              </div>
            <p>{{item.desc}}</p>
            </div>
        </swiper-slide>
       <div class="swiper-pagination btn"  slot="pagination">
       </div>
    </swiper>
  </div>
</template>
<script>
export default {
  name: 'HomeIcons',
  props: {
    iconList: Array
  },
  data: function () {
    return {
      swiperOption: {
        pagination: '.swiper-pagination'
      }
    }
  },
  computed: {
    pages: function () {
      var pages = []
      this.iconList.forEach(function (item, index) {
        var page = Math.floor(index / 8)
        if (!pages[page]) {
          pages[page] = []
        }
        pages[page].push(item)
      })
      return pages
    }
  }
}
</script>
<style lang='stylus' scoped>
.icons >>> .swiper-pagination-bullet-active
    background: blue !important
.icons >>> .swiper-container
    height: 0
    overflow: hidden
    padding-bottom: 50%
.icons
  padding-top: .2rem
  padding-bottom: .2rem
.icon
  width: 25%
  float: left
  padding-bottom: 25%
  height: 0
  position: relative
  overflow: hidden
  .icon-img
    position: absolute
    bottom: .3rem
    width: 100%
    left: 0
    right: 0
    top: 0
    padding-top: .1rem
    .icon-img-content
      height: 80%
      display: block
      margin:0 auto
  p
    position: absolute
    left: 0
    right: 0
    bottom: .2rem
    text-align: center
</style>
