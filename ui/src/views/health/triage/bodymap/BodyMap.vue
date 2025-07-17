<template>
  <!-- <div class="header">
    <p>{{ clickedName || '点击身体部位' }}</p>
  </div> -->
  <div class="bodies">
    <div>
      <p>正面</p>
      <BodyContainer>
        <BodyPart
          v-for="(item, index) in antBodyParts"
          :key="index"
          :id="item.id"
          :d="item.d"
          :fill="getFill(item.id)"
          :click="handleClick"
          :mouseenter="handleMouseEnter"
          :mouseleave="handleMouseLeave" />
      </BodyContainer>
    </div>
    <div>
      <p>背面</p>
      <BodyContainer>
        <BodyPart
          v-for="(item, index) of postBodyPart"
          :key="index"
          :id="item.id"
          :d="item.d"
          :fill="getFill(item.id)"
          :click="handleClick"
          :mouseenter="handleMouseEnter"
          :mouseleave="handleMouseLeave" />
      </BodyContainer>
    </div>
  </div>
</template>

<script setup>
  import { reactive, computed } from 'vue'
  import BodyContainer from './BodyContainer.vue'
  import BodyPart from './BodyPart.vue'
  import { getBodyPart } from './bodyparts'

  const emit = defineEmits(['change'])

  const state = reactive({
    clicked: null,
    hovered: null,
  })

  const antBodyParts = getBodyPart('zh').filter(({ face }) => face === 'ant')
  const postBodyPart = getBodyPart('zh').filter(({ face }) => face === 'post')

  const clickedName = computed(() => {
    if (typeof state.clicked !== 'number' && !state.clicked) return ''
    const name = getBodyPart('zh').find(item => item.id === state.clicked).name || ''
    return name
  })

  const getFill = id => {
    if (state.clicked === id) {
      return 'rgb(255, 59, 48)'
    }
    if (state.hovered === id) {
      return 'rgb(85, 85, 87)'
    }
    return 'rgb(75, 75, 77)'
  }

  const handleClick = id => {
    state.clicked = id
    const name = getBodyPart('zh').find(item => item.id === state.clicked)?.name || ''
    emit('change', name)
  }

  const handleMouseEnter = id => {
    if ('ontouchstart' in window) return
    state.hovered = id
  }

  const handleMouseLeave = () => {
    if ('ontouchstart' in window) return
    state.hovered = null
  }
</script>

<style scoped>
  .header {
    position: fixed;
    left: 0;
    top: 0;
    width: 100%;
    height: 70px;
    background: rgba(19, 19, 21, 0.5);
    backdrop-filter: blur(10px);
    border-bottom: 1px solid rgb(27, 27, 27);
    color: rgb(255, 59, 48);
    z-index: 1200;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
  }

  .header p {
    margin: 0 0 5px;
    text-transform: uppercase;
    font-size: 14px;
  }

  .bodies {
    width: 90%;
    max-width: 500px;
    margin: 0 auto;
    padding: 50px 0;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .bodies p {
    color: rgb(48, 48, 48);
    text-transform: uppercase;
    font-size: 13px;
    text-align: center;
  }

  @media (max-width: 1024px) {
    .bodies {
      flex-direction: column;
    }
  }
</style>
