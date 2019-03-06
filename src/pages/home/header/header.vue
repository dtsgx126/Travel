<template>
    <div class="header">
     <div class="header-left">
        左箭头
     </div>
     <div class="header-input">
        请输入信息
     </div>
     <div class="header-right">
        北京
     </div>
    </div>
</template>

<script>
export default {
  name: 'HomeHeader'
}
</script>

<style lang='stylus' scoped>
  .header
      background:gray
      display:flex
      height:.86rem
      line-height:.86rem
      padding:.1rem
    .header-input
      flex:1
      background:#fff
      border-radius:.1rem
    .header-right
      padding-right:.2rem
</style>
