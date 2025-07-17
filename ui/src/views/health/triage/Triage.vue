<template>
  <div class="title">分诊导诊</div>
  <body-map @change="bodyNameChange" />
  <div class="input">
    <el-form label-width="auto">
      <el-form-item label="年龄">
        <el-input v-model="state.sex" placeholder="请输入年龄" />
      </el-form-item>
      <el-form-item label="年龄">
        <el-input v-model="state.age" placeholder="请输入年龄" />
      </el-form-item>
      <el-form-item label="症状">
        <el-input
          v-model="state.text"
          :rows="5"
          type="textarea"
          placeholder="请输入症状用于智能导诊" />
      </el-form-item>
    </el-form>
  </div>
  <div class="buttons">
    <input ref="file" type="file" class="file" />
    <el-button type="primary" @click="openFile">门诊数据</el-button>
    <el-button type="primary" @click="submit" :loading="state.loading">智能导诊</el-button>
    <el-button type="primary" @click="clean">清空内容</el-button>
  </div>
  <div v-if="state.result" v-html="state.result" class="content"></div>
</template>

<script setup>
  import { reactive, useTemplateRef, nextTick } from 'vue'
  import markdownit from 'markdown-it'
  import http from '../../../utils/http'
  import BodyMap from './bodymap/BodyMap.vue'

  const state = reactive({
    loading: false,
    sex: '男',
    age: 30,
    text: '',
    fileRef: useTemplateRef('file'),
    result: '',
  })

  const md = markdownit()

  function bodyNameChange(name) {
    state.text = `患者性别：${state.sex}\n患者年龄：${state.age}\n患者症状：${name + '不舒服'}`
  }

  function openFile() {
    state.fileRef.click()
  }

  async function submit() {
    const file = state.fileRef.files[0]
    if (!file) {
      ElMessage.error('请选择门诊数据')
      return
    }
    state.loading = true
    const formData = new FormData()
    formData.append('file', file)
    formData.append('text', state.text)
    const res = await http.post('/api/triage', formData)
    state.result = md.render(res.data.data.replace(/<think>[\s\S]*?<\/think>/g, ''))
    state.loading = false
    await nextTick()
    document.documentElement.scrollTo({
      top: document.documentElement.scrollHeight,
      behavior: 'smooth',
    })
  }

  function clean() {
    state.text = ''
    state.result = ''
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

  .file {
    width: 0;
    height: 0;
    opacity: 0;
  }

  .content {
    border: 1px solid #cccccc;
    margin-top: 10px;
    padding: 10px;
  }
</style>
