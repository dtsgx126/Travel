<template>
  <div class="wrap">
    <div class="item-list"
      v-for='(item,key) of cities'
      :key='key'
    >{{key}}
    </div>

  </div>
</template>
<script>

export default{
  name: 'Alphabet',
  props: {
    cities: Object
  }
}
</script>
<style lang='stylus' scoped>
@import '~styles/varibles.styl'
.wrap
  display: flex
  position: absolute
  top: 2.1rem
  right: 0
  bottom: 0
  flex-direction: column
  justify-content: center
  width: .4rem
  align-items: center
  font-size: .3rem
  color: $bgColor
  .item-list
    margin-bottom: .05rem
</style>
