<template>
  <div class="wrap" ref="wrapper">
    <div>
      <div class="area">
        <div class="title">当前城市</div>
        <div class="list">
          <div class="btn-wrap">
            <div class="btn">郑州</div>
          </div>
        </div>
      </div>
      <div class="area">
        <div class="title">热门城市</div>
        <div class="list">
          <div class="btn-wrap">
            <div class="btn">郑州</div>
          </div>
          <div class="btn-wrap">
            <div class="btn">郑州</div>
          </div>
          <div class="btn-wrap">
            <div class="btn">郑州</div>
          </div>
          <div class="btn-wrap">
            <div class="btn">郑州</div>
          </div>
          <div class="btn-wrap">
            <div class="btn">郑州</div>
          </div>
        </div>
      </div>
      <div class="area">
        <div class="title">A</div>
        <div class="list-item">
          <div class="item">阿拉尔</div>
          <div class="item">阿拉尔</div>
          <div class="item">阿拉尔</div>
          <div class="item">阿拉尔</div>
          <div class="item">阿拉尔</div>

        </div>
      </div>
      <div class="area">
        <div class="title">B</div>
        <div class="list-item">
          <div class="item">布格格</div>
          <div class="item">布格格</div>
          <div class="item">布格格</div>
          <div class="item">布格格</div>
          <div class="item">布格格</div>
          <div class="item">布格格</div>
          <div class="item">布格格</div>
          <div class="item">布格格</div>
          <div class="item">布格格</div>
          <div class="item">布格格</div>

        </div>
      </div>
    </div>
  </div>
</template>
<script>
import Bscroll from 'better-scroll'
export default{
  name: 'CityList',
  mounted: function () {
    this.scroll = new Bscroll(this.$refs.wrapper)
  }
}
</script>
<style lang='stylus' scoped>
.wrap
  position: absolute
  top: 2.1rem
  left: 0
  right: 0
  bottom: 0
  overflow: hidden
  .area
    overflow: hidden
    border-bottom: 1px solid #ccc
    .title
      background: #ccc
      text-indent: .2rem
      height: .7rem
      line-height: .7rem
    .list
      padding:.1rem .6rem .1rem .1rem
      .btn-wrap
        width: 33.3%
        float: left
        .btn
          margin:0.3rem auto
          max-width: 1rem
          min-width: 1.5rem
          border:1px solid #ddd
          text-align: center
          padding:.1rem .3rem
          border-radius: .1rem
    .list-item
      text-indent: .2rem
      .item
        width: 100%
        border-bottom:1px solid #ddd
        padding-top: .15rem
        padding-bottom: .15rem

</style>
