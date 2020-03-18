<template>
  <p>
    <template v-for="(value) in obj" >
      <template v-if="value.type == 'EOL'">
        <span v-bind:key='value.index' class='special' v-b-popover.hover.top="value.type" :title="value.index">
          \n<br/>
        </span>
      </template>
      <template v-else-if="value.type == 'container'">
        <span v-bind:key='value.index'>
          <b-link v-html='value.value[0] + "..." + value.value[value.value.length - 1]'
            :id="'popover-' + value.index + '-' + value.value.length"
          ></b-link>
          <b-popover :target="'popover-' + value.index + '-' + value.value.length" triggers="hover click" placement="bottom" >
            <template v-slot:title>
              <span v-html="value.index + ' - ' + value.type"></span>
            </template>
            <b-card style="background-color: black; border: 2px solid aquamarine;">
              <token-visual :obj="tokenizer(value.value.slice(1, value.value.length - 1))" :tokenizer="tokenizer" />
            </b-card>
          </b-popover>
        </span>
      </template>
      <template v-else>
        <span v-bind:key='value.index'
            v-html='value.value' v-b-popover.hover.top="value.type" :title="value.index"
            :class='value.type'
        ></span>
      </template>
    </template>
  </p>
</template>

<script>
export default {
  name: 'token-visual',
  props: ['obj', 'tokenizer']
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