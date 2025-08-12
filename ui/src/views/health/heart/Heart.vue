<template>
  <div class="title">心脏超声</div>
  <div class="buttons">
    <input type="file" class="file" ref="file" accept="video/mp4" />
    <el-button type="primary" :loading="state.loading" @click="submit">上传超声视频</el-button>
    <el-button type="primary" :disabled="state.loading" @click="reset">重置</el-button>
    <span class="status">{{ state.status }}</span>
  </div>
  <div class="video" v-if="state.src">
    <video
      ref="video"
      :src="state.src"
      controls
      loop
      muted
      autoplay
      width="224"
      height="224"></video>
  </div>
  <div v-html="state.result" class="result"></div>
  <div v-html="state.suggestion" class="suggestion"></div>
</template>

<script setup>
  import { reactive, useTemplateRef, onMounted } from 'vue'
  import http from '../../../utils/http'
  import markdownit from 'markdown-it'

  const md = markdownit()

  const state = reactive({
    result: '',
    file: useTemplateRef('file'),
    video: useTemplateRef('video'),
    src: '',
    loading: false,
    status: '',
    suggestion: '',
  })

  onMounted(() => {
    state.file.addEventListener('change', async () => {
      if (state.file.files.length === 0) {
        return
      }
      state.src = URL.createObjectURL(state.file.files[0])
      state.loading = true
      state.status = '正在分析...'
      const formData = new FormData()
      formData.append('file', state.file.files[0])
      let res = await http.post('/api/heart', formData)
      let result = ''
      for (const [key, value] of Object.entries(res.data.data)) {
        result += `<span style="color:blue">${key}</span>：<span style="color:red">${value}</span><br>`
      }
      state.result = result

      state.status = '正在生成诊疗建议...'

      const q = `
      <result>${state.result}</result>
      <result>为心脏超声检测结果，根据超声检测结果，生成诊疗建议。
      `
      res = await http.post('/api/form', { prompt: q })

      const answer = res.data.data.replace(/<think>[\s\S]*?<\/think>/g, '')
      state.suggestion = md.render(answer)

      state.status = ''
      state.loading = false
    })
  })

  const submit = async () => {
    state.file.click()
  }

  const reset = () => {
    state.file.value = null
    state.src = ''
    state.result = ''
    state.suggestion = ''
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

  .buttons {
    margin-top: 10px;
  }

  .video {
    margin-top: 10px;
  }

  .file {
    width: 0;
    height: 0;
  }

  .status {
    margin-left: 10px;
    color: #aaaaaa;
  }

  .result {
    margin-top: 10px;
  }
</style>
