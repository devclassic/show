<template>
  <path
    :id="props.id"
    :d="props.d"
    @click="handleClick"
    @mouseenter="handleMouseEnter"
    @mouseleave="handleMouseLeave"
    :style="style" />
</template>

<script setup>
  import { computed } from 'vue'

  const props = defineProps(['id', 'd', 'fill', 'click', 'mouseenter', 'mouseleave'])

  const handleClick = () => {
    props.click(props.id)
  }

  const handleMouseEnter = () => {
    props.mouseenter(props.id)
  }

  const handleMouseLeave = () => {
    props.mouseleave(props.id)
  }

  const style = computed(() => {
    return Object.assign(
      {},
      { WebkitTapHighlightColor: 'transparent', cursor: 'pointer' },
      { fill: props.fill },
    )
  })
</script>
