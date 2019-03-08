<template>
  <div class="icons">
    <swiper :options="swiperOption">
        <swiper-slide v-for='(page,index) of pages' :key='index'>
            <div class="icon" v-for='item of page' :key='item.id'>
              <div class="icon-img">
              <img class="icon-img-content" :src="item.iconUrl">
              </div>
            <p>景点门票</p>
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
  data: function () {
    return {
      swiperOption: {
        pagination: '.swiper-pagination'
      },
      iconList: [{
        id: '0001',
        iconUrl: 'http://img1.qunarzz.com/piao/fusion/1803/95/f3dd6c383aeb3b02.png',
        desc: '门票景点'
      }, {
        id: '0002',
        iconUrl: 'http://img1.qunarzz.com/piao/fusion/1804/5a/13ceb38dcf262f02.png',
        desc: '一日游'
      }, {
        id: '0003',
        iconUrl: 'http://img1.qunarzz.com/piao/fusion/1804/ff/fdf170ee89594b02.png',
        desc: '郑州必看'
      }, {
        id: '0004',
        iconUrl: 'http://img1.qunarzz.com/piao/fusion/1803/95/8246f27355943202.png',
        desc: '海洋馆'
      }, {
        id: '0005',
        iconUrl: 'http://img1.qunarzz.com/piao/fusion/1803/95/f3dd6c383aeb3b02.png',
        desc: '踏青赏月'
      }, {
        id: '0006',
        iconUrl: 'http://img1.qunarzz.com/piao/fusion/1803/95/f3dd6c383aeb3b02.png',
        desc: '世界之窗'
      }, {
        id: '0007',
        iconUrl: 'http://img1.qunarzz.com/piao/fusion/1803/95/f3dd6c383aeb3b02.png',
        desc: '动植物园'
      }, {
        id: '0008',
        iconUrl: 'http://img1.qunarzz.com/piao/fusion/1803/95/f3dd6c383aeb3b02.png',
        desc: '玩转长龙'
      }, {
        id: '0009',
        iconUrl: 'http://img1.qunarzz.com/piao/fusion/1803/95/f3dd6c383aeb3b02.png',
        desc: '华侨城'
      }
      ]
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
