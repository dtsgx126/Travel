<template>
    <div>
      <div class="title">热销组件</div>
      <ul>
        <li class="item border-bottom" v-for='item of recommendList' :key='item.id'>
          <div class="img-wrap"><img :src="item.imgUrl" alt=""></div>
          <div class="item-info">
            <p class="item-title">{{item.title}}</p>
            <p class="item-desc">{{item.desc}}</p>
            <button>查看详情</button>
          </div>
        </li>
      </ul>
    </div>
</template>
<script>
export default{
  name: 'HomeRecommend',
  props: {
    recommendList: Array
  }
}
</script>
<style lang='stylus' scoped>
@import '~styles/varibles.styl'
.title
  background: #ccc
  padding-top:.15rem
  padding-bottom: .15rem
  text-indent: $leftEdge
  line-height: .5rem
.item
  display: flex
  padding: $leftEdge
  .item-info
    flex: 1
    display: flex
    flex-direction: column
    justify-content: space-around
    align-items: end
    padding-left: $leftEdge
    .item-title
      font-size: .4rem
    .item-desc
      color: gray
    button
      padding: .1rem
      border-radius: .1rem
      background #ff9300
  .img-wrap
    width: 25%
    img
      width: 100%

</style>
