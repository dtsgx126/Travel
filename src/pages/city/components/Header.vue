<template>
  <div class="header">
    <router-link to='/' class='link'>
      <span class="iconfont">&#xe624;</span>
    </router-link>
    <div class="btn-wrap">
      <button class="btn active">境内</button>
      <button class="btn">国际/地区</button>
    </div>

  </div>
</template>
<script>
export default {
  name: 'CityHeader'
}
</script>
<style lang='stylus' scoped>
@import '~styles/varibles.styl'
.header
  position: relative
  display: flex
  background: $bgColor
  justify-content: center
  height: 1rem
  align-items: center
  .btn-wrap
    display: flex
    justify-content: center
    border-radius: .1rem
    overflow: hidden
    height: .6rem
    border:.1rem solid #fff
    font-weight: 900
    border-sizing:border-box
    outline: none
    .btn
      width: 2rem
      display: inline-block
      border-top-right-radius: .01rem
      border-bottom-right-radius: .01rem
    .active
      background: #fff
  .link
    position: absolute
    left: $leftEdge
    line-height: .86rem
    color: #fff

</style>
