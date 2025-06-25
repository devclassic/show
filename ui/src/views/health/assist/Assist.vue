<template>
  <div class="title">辅助诊疗</div>
  <div class="input">
    <el-input v-model="state.text" :rows="5" type="textarea" placeholder="请输入内容用于辅助诊疗" />
  </div>
  <div class="buttons">
    <el-button type="primary" :loading="state.loading" @click="submit">辅助诊疗</el-button>
    <el-button type="primary" @click="clean">清空内容</el-button>
  </div>
  <div ref="content" class="content">
    <div v-for="item in state.messages" :key="item.role">
      <div v-if="item.role == 'user'" style="color: blue">{{ item.content }}</div>
      <div v-else style="color: red" v-html="item.content"></div>
    </div>
  </div>
</template>

<script setup>
  import { reactive, useTemplateRef, nextTick } from 'vue'
  import markdownit from 'markdown-it'
  import http from '../../../utils/http'

  const state = reactive({
    contentRef: useTemplateRef('content'),
    loading: false,
    text: '',
    messages: [
      { role: 'user', content: '你好' },
      { role: 'ai', content: '你好' },
    ],
  })

  const md = markdownit()

  state.messages = []

  function clean() {
    state.text = ''
    state.messages = []
  }

  async function submit() {
    if (!state.text) {
      ElMessage.error('请输入内容')
      return
    }
    state.messages.push({ role: 'user', content: state.text })
    await nextTick()
    state.contentRef.scrollTo({
      top: state.contentRef.scrollHeight,
      behavior: 'smooth',
    })
    state.loading = true
    const res = await http.post('/api/assist', { question: state.text })
    console.log(res)
    const answer = res.data.data.replace(/<think>[\s\S]*?<\/think>/g, '')
    state.messages.push({ role: 'ai', content: md.render(answer) })
    await nextTick()
    state.contentRef.scrollTo({
      top: state.contentRef.scrollHeight,
      behavior: 'smooth',
    })
    state.text = ''
    state.loading = false
  }
</script>

<style scoped>
  .title {
    font-size: 20px;
    font-weight: bold;
    color: #555555;
  }

  .input {
    margin-top: 10px;
  }

  .buttons {
    margin-top: 10px;
  }

  .content {
    border: 1px solid #cccccc;
    margin-top: 10px;
    padding: 10px;
    height: calc(100vh - 330px);
    overflow: auto;
  }
</style>
