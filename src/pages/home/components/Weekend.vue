<template>
    <div class="weekend">
      <div class="title">周末去哪玩</div>
      <ul>
        <li class="item border-bottom" v-for='item of weekendList' :key='item.id'>
          <div class="img-wrap"><img :src="item.imgUrl" alt=""></div>
            <p class="item-title">{{item.title}}</p>
            <p class="item-desc">{{item.desc}}</p>
        </li>
      </ul>
    </div>
</template>
<script>
export default{
  name: 'HomeWeekend',
  props: {
    weekendList: Array
  }
}
</script>
<style lang='stylus' scoped>
@import '~styles/varibles.styl'
.weekend
  background: #ccc
.title
  background: #ccc
  padding-top:.15rem
  padding-bottom: .15rem
  text-indent: $leftEdge
  line-height: .5rem
.item
  background: #fff
  display: flex
  flex-direction: column
  justify-content: space-around
  align-items: end
  padding-bottom: .3rem
  margin-bottom: .1rem
  .item-title
    text-indent: $leftEdge
    font-size: .3rem
    line-height: .5rem
    padding-top: .3rem
  .item-desc
    text-indent: $leftEdge
    color: #616161
    line-height: .5rem
  img
    width: 100%

</style>
