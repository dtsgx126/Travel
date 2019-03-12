<template>
  <div class="wrap">
    <div class="item-list" v-for='item of letters' :key='item'
        :ref='item'
        @click='handleLetterClick'
        @touchstart='handleTouchStart'
        @touchmove='handleTouchMove'
        @touchend='handleTouchEnd'
    >{{item}}
    </div>

  </div>
</template>
<script>

export default{
  name: 'Alphabet',
  props: {
    cities: Object
  },
  data: function () {
    return {
      touchStatus: false,
      startY: 0,
      timer: null
    }
  },
  updated () {
    this.startY = this.$refs['A'][0].offsetTop
  },
  computed: {
    letters: function () {
      var letters = []
      for (let i in this.cities) {
        letters.push(i)
      }
      return letters
    }
  },
  methods: {
    handleLetterClick (e) {
      this.$emit('change', e.target.innerText)
    },
    handleTouchStart () {
      this.touchStatus = true
    },
    handleTouchMove (e) {
      if (this.touchStatus) {
        if (this.timer) {
          clearTimeout(this.timer)
        }
        this.timer = setTimeout(() => {
          var eleHight = this.$refs['A'][0].offsetHeight
          var moveY = e.touches[0].clientY
          var index = Math.floor((moveY - this.startY) / eleHight)
          if (index >= 0 && index < this.letters.length) {}
          this.$emit('change', this.letters[index])
        }, 16)
      }
    },
    handleTouchEnd () {
      this.touchStatus = false
    }
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
