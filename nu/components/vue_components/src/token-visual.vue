<template>
  <p>
    <template v-for="(value) in obje" >
      <span v-bind:key="value.index" v-html="value.value">
      </span>
    </template>
  </p>
</template>

<script>
export default {
  name: 'token-visual',
  props: ['obj', 'tokenizer', 'vueapp'],
  data() {
    console.log(this.tokenizer, this.obj, this.vueapp)
    if (this.vueapp === true) {
      return {
        obje: this.obj,
        toke: this.tokenizer,
      }
    } else {
      return {
        obje: window[this.obj],
        toke: window[this.tokenizer],
      }
    }
  },
  mounted() {
    console.log('token-visual', this.obj, this.tokenizer, window[this.obj])
  },
}
</script>


<style scoped>

.char {
  color: crimson;
}

.special {
  color: darkmagenta;
}

.symbol {
  color: darkkhaki;
}

.literal_string {
  color: darkseagreen;
}

.container {
  color: aquamarine;
}

</style>