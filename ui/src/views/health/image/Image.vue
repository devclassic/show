<template>
  <div class="title">医学影像</div>
  <div class="input">
    <el-form label-width="auto">
      <el-form-item label="影像">
        <input type="file" ref="file" class="file" accept="image/*" multiple />
        <el-button type="primary" @click="openfile">上传图片</el-button>
        <el-button type="primary" @click="submit" :loading="state.loading">提交</el-button>
        <el-button type="primary" @click="reset">重置</el-button>
      </el-form-item>
      <el-form-item label="提示词">
        <el-input
          v-model="state.text"
          :rows="5"
          type="textarea"
          placeholder="请输入症状用于智能导诊" />
      </el-form-item>
    </el-form>
  </div>
  <div class="result">
    <div
      v-for="item in state.messages"
      :class="{
        user: item.role === 'user',
        assistant: item.role === 'assistant',
      }"
      class="item">
      {{ item.content }}
    </div>
  </div>
</template>

<script setup>
  import { reactive, useTemplateRef, onMounted } from 'vue'
  import http from '../../../utils/http'
  import { ElMessage } from 'element-plus'

  const state = reactive({
    loading: false,
    file: useTemplateRef('file'),
    text: '',
    messages: [],
  })

  onMounted(() => {
    reset()
  })

  function openfile() {
    state.file.click()
  }

  async function submit() {
    state.loading = true
    state.messages.push({
      role: 'user',
      content: state.text,
    })
    const formData = new FormData()
    for (let i = 0; i < state.file.files.length; i++) {
      formData.append('files', state.file.files[i])
    }
    formData.append('text', state.text)
    state.text = ''
    const res = await http.post('/api/image', formData)
    state.messages.push({
      role: 'assistant',
      content: res.data.data,
    })
    state.loading = false
    state.file.value = ''
  }

  async function reset() {
    state.messages = []
    state.file.value = ''
    state.text = ''
    const res = await http.post('/api/image/reset')
    console.log(res.data)
    ElMessage.success('重置成功')
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

  .file {
    width: 0;
    height: 0;
  }

  .result {
    margin-top: 10px;
  }

  .user {
    color: blue;
  }

  .assistant {
    color: red;
  }

  .item {
    margin-bottom: 10px;
  }
</style>
