<template>
    <div>
      <div class="title">热销组件</div>
      <ul>
        <li class="item border-bottom" v-for='item of itemList' :key='item.id'>
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
  data: function () {
    return {
      itemList: [{
        id: '0001',
        imgUrl: 'http://img1.qunarzz.com/sight/p0/1708/d6/d6f00849ce9c0eaea3.img.jpg_200x200_624d720f.jpg',
        title: '香堤湾温泉',
        desc: '回归自然、放飞心情、陶冶情操的佳处'
      }, {
        id: '0002',
        imgUrl: 'http://img1.qunarzz.com/sight/p0/1709/e9/e9b7ae23f567806ea3.img.jpg_200x200_bf985a3d.jpg',
        title: '郑州方特',
        desc: '🔥好评如潮，小伙伴热推景点~'
      }, {
        id: '0003',
        imgUrl: 'http://img1.qunarzz.com/sight/p0/1609/bf/bf08848479f88943a3.img.png_200x200_97bac4f8.png',
        title: '登封大熊山',
        desc: '风光旖旎，森林密布，有千年古刹香峪寺'
      }, {
        id: '0004',
        imgUrl: 'http://img1.qunarzz.com/sight/p0/1505/ce/ceacda87f56ae8e3.water.jpg_200x200_8585abf4.jpg',
        title: '康百万庄园',
        desc: '👍小伙伴们都收藏了，去看看吧~'
      }, {
        id: '0005',
        imgUrl: 'http://img1.qunarzz.com/sight/p0/1708/d6/d6f00849ce9c0eaea3.img.jpg_200x200_624d720f.jpg',
        title: '香堤湾温泉',
        desc: '一场贯彻快乐的艺术盛宴'
      }
      ]
    }
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
