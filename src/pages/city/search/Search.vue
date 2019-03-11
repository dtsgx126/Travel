<template>
  <div class="search">
    <span class="iconfont ico-search">&#xe632;</span>
    <input class="content" type="text" placeholder="请输入城市">
  </div>
</template>
<script>
export default {
  name: 'CitySearch'
}
</script>
<style lang='stylus' scoped>
@import '~styles/varibles.styl'
.search
  background: $bgColor
  padding:.1rem
  heigth: .5rem
  display: flex
  position: relative
  font-size: .5rem
  .ico-search
    position:absolute
    line-height: .5rem
    left: .5rem
    top: .3rem
    font-size: .6rem
  .content
    flex: 1
    padding: .2rem
    width: 100%
    height: .5rem
    border-radius: .1rem
    text-align: center

</style>
