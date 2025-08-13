<template>
  <div class="title">数据分析</div>
  <el-form label-width="auto" class="form">
    <el-form-item label="文件">
      <input type="file" ref="file" class="file" multiple />
      <el-button type="primary" :disabled="state.loading" @click="upload">上传文件</el-button>
      <el-button type="primary" :loading="state.loading" @click="submit">分析</el-button>
      <el-button type="primary" :disabled="state.loading" @click="reset">重置</el-button>
      <div v-if="state.filenames.length" class="files">
        <div v-for="item in state.filenames" :key="item" class="file-item">{{ item }}</div>
      </div>
    </el-form-item>
    <el-form-item label="提示词">
      <el-input
        v-model="state.prompt"
        :rows="5"
        type="textarea"
        placeholder="请输入症状用于智能导诊" />
    </el-form-item>
  </el-form>
  <div class="result" v-html="state.result"></div>
</template>

<script setup>
  import { reactive, useTemplateRef, onMounted } from 'vue'
  import http from '../../../utils/http'
  import markdownit from 'markdown-it'

  const md = markdownit()

  const state = reactive({
    file: useTemplateRef('file'),
    filenames: [],
    prompt: '',
    loading: false,
    result: '',
  })

  onMounted(() => {
    state.file.addEventListener('change', e => {
      const files = e.target.files
      if (files.length > 10) {
        ElMessage.error('最多上传10个文件')
        e.target.value = ''
        state.filenames = []
        return
      }
      state.filenames = []
      for (const file of files) {
        state.filenames.push(file.name)
      }
    })
  })

  function upload() {
    state.file.click()
  }

  async function submit() {
    state.loading = true
    const formData = new FormData()
    formData.append('prompt', state.prompt)
    for (const file of state.file.files) {
      formData.append('files', file)
    }
    const res = await http.post('/api/analysis', formData)
    console.log(res.data)
    const result = res.data.data.data.outputs.text.replace(/<think>[\s\S]*?<\/think>/g, '')
    state.result = md.render(result)
    state.loading = false
  }

  function reset() {
    state.file.value = ''
    state.filenames = []
    state.prompt = ''
    state.result = ''
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

  .form {
    margin-top: 10px;
  }

  .file {
    width: 0;
    height: 0;
  }

  .files {
    width: 100%;
    margin-top: 10px;
  }

  .file-item {
    border: 1px solid #ccc;
    padding: 5px 10px;
    color: #555555;
    margin-bottom: 10px;
  }

  .file-item:last-child {
    margin-bottom: 0;
  }

  .result {
    color: red;
  }
</style>
