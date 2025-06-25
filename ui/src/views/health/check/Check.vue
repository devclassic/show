<template>
  <div class="title">内涵质控</div>
  <el-form label-width="auto" class="form">
    <el-form-item label="类型">
      <el-input v-model="state.type" placeholder="请输入质控类型" />
    </el-form-item>
    <el-form-item label="内容">
      <el-input v-model="state.content" type="textarea" :rows="8" placeholder="请输入质控内容" />
    </el-form-item>
  </el-form>
  <div class="buttons">
    <el-button :loading="state.loading" type="primary" @click="check">运行内涵质控</el-button>
    <el-button type="primary" @click="clean">清空内容</el-button>
  </div>
  <div v-if="state.result" v-html="state.result" class="result"></div>
</template>

<script setup>
  import { reactive } from 'vue'
  import markdownit from 'markdown-it'
  import http from '../../../utils/http'

  const state = reactive({
    loading: false,
    type: '',
    content: '',
    result: '',
  })

  const md = markdownit()

  async function check() {
    if (!state.type) {
      ElMessage.error('请输入质控类型')
      return
    }
    if (!state.content) {
      ElMessage.error('请输入质控内容')
      return
    }
    state.loading = true
    const res = await http.post('/api/check', {
      type: state.type,
      content: state.content,
    })
    const text = res.data.data.replace(/<think>[\s\S]*?<\/think>/g, '')
    state.result = md.render(text)
    state.loading = false
  }

  const clean = () => {
    state.type = ''
    state.content = ''
    state.result = ''
  }
</script>

<style scoped>
  .title {
    font-size: 20px;
    font-weight: bold;
    color: #555555;
  }

  .form {
    margin-top: 10px;
  }

  .result {
    border: 1px solid #cccccc;
    margin-top: 10px;
    padding: 10px;
  }
</style>
