<template>
  <div id="app">
    <nu-call>Hello There</nu-call>
    <token-visual :obj="data" :tokenizer="tokenizer" :vueapp="true"></token-visual>
  </div>
</template>

<script>
import TokenVisual from './token-visual.vue'
import NuCall from './nu-call.vue'
import tokenizer from './js_tokenizer.js'

export default {
  name: 'App',
  data() {
    return {
      tokenizer,
      data: [{type: 'symbol', value: 'hello', index:0},
              {type: 'space', value: ' ', index:4},
              {type: 'symbol', value: 'there', index:5}]
    }
  },
  components: {
    TokenVisual, NuCall
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
