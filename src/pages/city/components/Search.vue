<template>
  <div class="search">
    <span class="iconfont ico-search">&#xe632;</span>
    <input class="content" type="text"
    v-model='searchInfo' placeholder="请输入城市/旅游景点">
    <div class="result-search"
        ref='selecity'
        v-show='searchInfo'
    >
      <div>
        <div class="item-city border-bottom"
          v-for='item of list'
          :key='item.id'
        >{{item.name}}
        </div>
        <div
          class="item-city border-bottom"
          v-show='!list.length'
        >没有找到匹配项
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import Bscroll from 'better-scroll'
export default {
  name: 'CitySearch',
  props: {
    cities: Object
  },
  data: function () {
    return {
      searchInfo: '',
      list: [],
      timer: null
    }
  },
  watch: {
    searchInfo: function () {
      if (this.timer) { clearTimeout(this.timer) }
      if (!this.searchInfo) {
        this.list = []
        return
      }
      this.timer = setTimeout(() => {
        var result = []
        for (let i in this.cities) {
          this.cities[i].forEach((value) => {
            if (value.spell.indexOf(this.searchInfo) > -1 ||
              value.name.indexOf(this.searchInfo) > -1) {
              result.push(value)
            }
          })
        }
        this.list = result
      }, 200)
    }
  },
  mounted: function () {
    this.scroll = new Bscroll(this.$refs.selecity)
  }

}
</script>
<style lang='stylus' scoped>
@import '~styles/varibles.styl'
.search
  background: $bgColor
  padding:.1rem
  heigth: .5rem
  font-size: .5rem
  .ico-search
    position: absolute
    left: .2rem
    top: 1.24rem
  .content
    box-sizing: border-box
    line-height: .5rem
    padding: .2rem
    width: 100%
    height: .5rem
    border-radius: .1rem
    text-align: center
    font-size: .4rem
  .result-search
    z-index: 1
    overflow: hidden
    position: absolute
    top: 1.74rem
    left :0
    right: 0
    bottom: 0
    background: #eee
    .item-city
      padding-top: .15rem
      padding-bottom: .15rem
      padding-left: .2rem
</style>
