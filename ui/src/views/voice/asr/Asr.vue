<template>
  <div class="title">语音识别</div>
  <div class="buttons">
    <el-button type="primary" @click="record">{{ state.btnRecordText }}</el-button>
    <el-button type="primary" @click="clean">清空内容</el-button>
    <span class="status">{{ state.status }}</span>
  </div>
  <div v-if="state.result" class="content">
    {{ state.result }}
  </div>
</template>

<script setup>
  import { reactive } from 'vue'
  import asr from '../../../utils/asr'
  import http from '../../../utils/http'

  const state = reactive({
    btnRecordText: '开始收音',
    status: '',
    result: '',
  })

  // asr.ontext = text => {
  //   console.log(text)
  //   state.result = text
  // }

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
        state.status = '正在处理...'
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
        state.result = res.data.data[0].text
      })
    }
  }

  function clean() {
    state.result = ''
  }
</script>

<style scoped>
  .title {
    font-size: 20px;
    font-weight: bold;
    color: #555555;
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
    padding: 10px;
    margin-top: 10px;
  }
</style>
