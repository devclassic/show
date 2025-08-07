<template>
  <div class="title">辅助诊疗</div>
  <div class="input">
    <el-input v-model="state.text" :rows="5" type="textarea" placeholder="请输入内容用于辅助诊疗" />
  </div>
  <div class="buttons">
    <el-button type="primary" :loading="state.loading" @click="submit">辅助诊疗</el-button>
    <el-button type="primary" @click="record">{{ state.btnRecordText }}</el-button>
    <el-button type="primary" @click="clean">清空内容</el-button>
    <span class="status">{{ state.status }}</span>
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
  import asr from '../../../utils/asr'

  const state = reactive({
    contentRef: useTemplateRef('content'),
    status: '',
    loading: false,
    text: '',
    btnRecordText: '开始收音',
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
    const q = state.text
    state.text = ''
    await nextTick()
    state.contentRef.scrollTo({
      top: state.contentRef.scrollHeight,
      behavior: 'smooth',
    })
    state.loading = true
    const res = await http.post('/api/assist', { question: q })
    const answer = res.data.data.replace(/<think>[\s\S]*?<\/think>/g, '')
    state.messages.push({ role: 'ai', content: md.render(answer) })
    await nextTick()
    state.contentRef.scrollTo({
      top: state.contentRef.scrollHeight,
      behavior: 'smooth',
    })
    state.loading = false
  }

  let isRecoding = false

  function record() {
    if (!isRecoding) {
      asr.start(
        () => {
          ElMessage.success('开始收音')
          state.btnRecordText = '停止收音'
          state.status = '正在收音...'
          isRecoding = true
        },
        () => {
          ElMessage.error('收音错误')
          state.status = ''
          state.btnRecordText = '开始收音'
          isRecoding = false
        },
      )
    } else {
      asr.stop(async () => {
        ElMessage.success('停止收音')
        state.status = '正在识别...'
        state.btnRecordText = '开始收音'
        isRecoding = false
        //处理语音上传
        const blob = asr.getWAVBlob()
        const file = new File([blob], 'audio.wav')
        const formData = new FormData()
        formData.append('file', file)
        const res = await http.post('/api/asr', formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        })
        state.status = ''
        state.text = res.data.data[0].text
      })
    }
  }
</script>

<style>
  table {
    width: 100%;
    border-collapse: collapse;
    margin: 20px 0;
  }

  table,
  th,
  td {
    border: 1px solid #ccc;
  }

  th {
    background-color: #f2f2f2;
    padding: 10px;
    text-align: left;
  }

  td {
    padding: 10px;
    text-align: left;
  }
</style>

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

  .status {
    margin-left: 10px;
    color: #aaaaaa;
  }

  .content {
    border: 1px solid #cccccc;
    margin-top: 10px;
    padding: 10px;
    height: calc(100vh - 330px);
    overflow: auto;
  }
</style>
