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
  height: .86rem
  align-items: center
  .btn-wrap
    display: flex
    justify-content: center
    border-radius: .1rem
    overflow: hidden
    height: .7rem
    border:.01rem solid #fff
    font-weight: 900
    .btn
      width: 2rem
    .active
      background: #fff
  .link
    position: absolute
    left: $leftEdge
    line-height: .86rem
    color: #fff

</style>
