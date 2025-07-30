<template>
  <div class="title">医学影像</div>
  <div class="input">
    <el-form label-width="auto">
      <el-form-item v-if="state.images.length" label="影像" class="imgitem">
        <span v-for="url of state.images" class="item">
          <img :src="url" height="100" class="img" />
        </span>
      </el-form-item>
      <el-form-item label="操作">
        <input type="file" ref="file" @change="fileChange" class="file" multiple />
        <input type="file" ref="filedcm" @change="fileDcmChange" class="file" multiple />
        <el-button type="primary" :loading="state.uploading" @click="openfile">上传图片</el-button>
        <el-button type="primary" :loading="state.uploading" @click="openfiledcm">
          上传DCM
        </el-button>
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
      <div v-if="item.images?.length" class="msgimg">
        <span v-for="url of item.images" class="msgimgitme">
          <img :src="url" height="100" class="img" />
        </span>
      </div>
      <div v-html="item.content"></div>
    </div>
  </div>
</template>

<script setup>
  import { reactive, useTemplateRef } from 'vue'
  import http from '../../../utils/http'
  import markdownit from 'markdown-it'

  const baseURL = import.meta.env.VITE_API_BASE_URL ?? ''
  const md = markdownit()

  const state = reactive({
    loading: false,
    uploading: false,
    file: useTemplateRef('file'),
    filedcm: useTemplateRef('filedcm'),
    files: [],
    images: [],
    text: '',
    messages: [],
    history: [
      {
        role: 'system',
        content: [
          {
            type: 'text',
            text: '你是端点科技医疗影像助手，你需要根据用户的症状和影像，给出诊断建议和治疗建议。用中文回答用户问题。',
          },
        ],
      },
    ],
    paths: [],
  })

  function openfile() {
    state.file.click()
  }

  function openfiledcm() {
    state.filedcm.click()
  }

  function fileChange() {
    state.uploading = true
    state.images = []
    state.files = state.file.files
    for (const file of state.files) {
      const reader = new FileReader()
      reader.onload = e => {
        state.images.push(e.target.result)
      }
      reader.readAsDataURL(file)
    }
    state.uploading = false
  }

  async function fileDcmChange() {
    state.uploading = true
    const formData = new FormData()
    for (const file of state.filedcm.files) {
      formData.append('files', file)
    }
    const res = await http.post('/api/updcm', formData)
    if (res.data.success) {
      state.images = res.data.data.images.map(item => baseURL + item)
      state.paths = res.data.data.paths
    } else {
      ElMessage.error(res.data.message)
    }
    state.uploading = false
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
    formData.append('paths', state.paths)
    state.text = ''
    const res = await http.post('/api/image', formData)
    state.messages.push({
      role: 'assistant',
      content: md.render(res.data.data.text),
    })
    state.history = res.data.data.history
    state.loading = false
    state.file.value = ''
    state.filedcm.value = ''
    state.paths = []
  }

  async function reset() {
    state.messages = []
    state.images = []
    state.file.value = ''
    state.filedcm.value = ''
    state.text = ''
    state.history = [
      {
        role: 'system',
        content: [
          {
            type: 'text',
            text: '你是端点科技医疗影像助手，你需要根据用户的症状和影像，给出诊断建议和治疗建议。用中文回答用户问题。',
          },
        ],
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
