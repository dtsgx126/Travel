<template>
    <div class="weekend">
      <div class="title">周末去哪玩</div>
      <ul>
        <li class="item border-bottom" v-for='item of itemList' :key='item.id'>
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
  data: function () {
    return {
      itemList: [{
        id: '0001',
        imgUrl: 'http://img1.qunarzz.com/sight/source/1505/86/57819390ea997c.jpg_r_640x214_00888590.jpg',
        title: '香堤湾温泉',
        desc: '回归自然、放飞心情、陶冶情操的佳处'
      }, {
        id: '0002',
        imgUrl: 'http://img1.qunarzz.com/sight/source/1811/d2/017059dd59b0ee.jpg_r_640x214_497664a4.jpg',
        title: '郑州方特',
        desc: '🔥好评如潮，小伙伴热推景点~'
      }, {
        id: '0003',
        imgUrl: 'http://img1.qunarzz.com/sight/source/1603/eb/7f570846b929d8.jpg_r_640x214_7caca563.jpg',
        title: '登封大熊山',
        desc: '风光旖旎，森林密布，有千年古刹香峪寺'
      }, {
        id: '0004',
        imgUrl: 'http://img1.qunarzz.com/sight/source/1811/2c/e5e2b086fc0c60.jpg_r_640x214_811a2da7.jpg',
        title: '康百万庄园',
        desc: '👍小伙伴们都收藏了，去看看吧~'
      }, {
        id: '0005',
        imgUrl: 'http://img1.qunarzz.com/sight/source/1505/86/57819390ea997c.jpg_r_640x214_00888590.jpg',
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
