<template>
  <div class="title">医学影像</div>
  <div class="input">
    <el-form label-width="auto">
      <el-form-item label="操作">
        <input type="file" ref="file" @change="fileChange" class="file" accept="image/*" multiple />
        <el-button type="primary" @click="openfile">上传图片</el-button>
        <el-button type="primary" @click="submit" :loading="state.loading">提交</el-button>
        <el-button type="primary" @click="reset">重置</el-button>
      </el-form-item>
      <el-form-item v-if="state.images.length" label="影像" class="imgitem">
        <span v-for="url of state.images" class="item">
          <img :src="url" height="100" class="img" />
        </span>
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
      <div v-if="item.images?.length" class="msgimg">
        <span v-for="url of item.images" class="msgimgitme">
          <img :src="url" height="100" class="img" />
        </span>
      </div>
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
    files: [],
    images: [],
    text: '',
    messages: [],
    history: [
      {
        role: 'user',
        content: [{ type: 'text', text: '用中文回答用户问题' }],
      },
      {
        role: 'user',
        content: [{ type: 'text', text: '你是端点科技医疗影像助手' }],
      },
    ],
  })
  
  function openfile() {
    state.file.click()
  }

  function fileChange() {
    state.images = []
    state.files = state.file.files
    for (const file of state.files) {
      const reader = new FileReader()
      reader.onload = e => {
        state.images.push(e.target.result)
      }
      reader.readAsDataURL(file)
    }
  }

  async function submit() {
    state.loading = true
    state.messages.push({
      role: 'user',
      images: state.images,
      content: state.text,
    })
    state.images = []
    const formData = new FormData()
    for (let i = 0; i < state.file.files.length; i++) {
      formData.append('files', state.file.files[i])
    }
    formData.append('text', state.text)
    formData.append('history', JSON.stringify(state.history))
    state.text = ''
    const res = await http.post('/api/image', formData)
    state.messages.push({
      role: 'assistant',
      content: res.data.data.text,
    })
    state.history = res.data.data.history
    state.loading = false
    state.file.value = ''
  }

  async function reset() {
    state.messages = []
    state.images = []
    state.file.value = ''
    state.text = ''
    state.history = [
      {
        role: 'user',
        content: [{ type: 'text', text: '用中文回答用户问题' }],
      },
      {
        role: 'user',
        content: [{ type: 'text', text: '你是端点科技医疗影像助手' }],
      },
    ]
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

  .imgitem {
    line-height: 0;
    margin-bottom: 0;
  }

  .img {
    margin-right: 10px;
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
