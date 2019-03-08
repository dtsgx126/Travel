<template>
    <div class="header">
       <div class="header-left">
       <span class="iconfont">&#xe624;</span>
       </div>
       <div class="header-input">
          <span class="iconfont">&#xe632;</span>
          输入城市/景点/游玩主题
       </div>
       <div class="header-right">
       <span class="iconfont">&#xe614;</span>
          {{this.city}}
       </div>
    </div>
</template>

<script>
export default {
  name: 'HomeHeader',
  props: {
    city: String
  }
}
</script>

<style lang='stylus' scoped>
@import '~styles/varibles.styl'
  .header
      background:$bgColor
      display:flex
      height:.86rem
      line-height:.86rem
      padding:.1rem
      align-items:center
    .header-left
      margin-right:.2rem
      margin-left:.2rem
      font-weight:bold
      color: #fff
    .header-input
      flex:1
      background:#fff
      border-radius:.1rem
      padding-left:.2rem
      height:.68rem
      line-height:.68rem
      .iconfont
        margin-right:.2rem
    .header-right
      padding-right:.1rem
      padding-left:.1rem
      color: #fff
      .iconfont
        float:right

</style>
