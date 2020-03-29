<template>
<a href="#">
  <slot/>
</a>
</template>

<script>
export default {
  name: 'nu-call',
  props: ['call']
}
</script>