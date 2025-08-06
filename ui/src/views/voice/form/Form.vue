<template>
  <div class="title">表单填写</div>
  <div class="buttons">
    <el-button type="primary" @click="record">{{ state.btnRecordText }}</el-button>
    <el-button type="primary" @click="clean">重置表单</el-button>
    <span class="status">{{ state.status }}</span>
  </div>
  <div v-if="state.result" class="result">{{ state.result }}</div>
  <el-form label-width="auto" class="form">
    <el-form-item label="姓名">
      <el-input v-model="state.form.xm" />
    </el-form-item>
    <el-form-item label="年龄">
      <el-input v-model="state.form.nl" />
    </el-form-item>
    <el-form-item label="性别">
      <el-input v-model="state.form.xb" />
    </el-form-item>
    <el-form-item label="身份证号">
      <el-input v-model="state.form.sfzh" />
    </el-form-item>
    <el-form-item label="联系方式">
      <el-input v-model="state.form.lxfs" />
    </el-form-item>
    <el-form-item label="症状">
      <el-input type="textarea" :rows="3" v-model="state.form.zz" />
    </el-form-item>
    <el-form-item label="主诉">
      <el-input type="textarea" :rows="3" v-model="state.form.zs" />
    </el-form-item>
    <el-form-item label="既往史">
      <el-input type="textarea" :rows="3" v-model="state.form.jws" />
    </el-form-item>
    <el-form-item label="个人家族史">
      <el-input type="textarea" :rows="3" v-model="state.form.grjzs" />
    </el-form-item>
  </el-form>
</template>

<script setup>
  import { reactive } from 'vue'
  import asr from '../../../utils/asr'
  import http from '../../../utils/http'

  const state = reactive({
    btnRecordText: '开始收音',
    status: '',
    result: '',
    form: {
      xm: '',
      nl: '',
      xb: '',
      sfzh: '',
      lxfs: '',
      zz: '',
      zs: '',
      jws: '',
      grjzs: '',
    },
  })

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
        async () => {
          ElMessage.error('收音错误')
          state.status = '正在处理...'
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
        let res = await http.post('/api/asr', formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        })
        state.status = ''
        state.result = res.data.data[0].text
        state.status = '正在处理...'
        const prompt = `
        <text>${state.result}</text>
        请分析<text>中的内容
        以JSON的形式输出，输出的JSON遵守以下的格式：
        {
          "xm":<姓名>,
          "nl":<年龄>,
          "xb":<性别>,
          "sfzh":<身份证号>,
          "lxfs":<联系方式>,
          "zz":<症状>,
          "zs":<主诉>,
          "jws":<既往史>,
          "grjzs":<个人家族史>
        }
        如果内容中没有对应的信息，请用""代替。
        只输出JSON不要输出其他内容。
        JSON内容中的数字使用阿拉伯数字。
        `
        res = await http.post('/api/form', { prompt })
        let json = res.data.data.replace(/<think>[\s\S]*?<\/think>/g, '')
        json = json.replace('```json', '').replace('```', '')
        const data = JSON.parse(json)
        state.form = data
        state.status = ''
      })
    }
  }

  function clean() {
    state.form = {
      xm: '',
      nl: '',
      xb: '',
      sfzh: '',
      lxfs: '',
      zz: '',
      zs: '',
      jws: '',
      grjzs: '',
    }
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

  .result {
    border: 1px solid #cccccc;
    padding: 10px;
    margin-top: 10px;
    overflow: auto;
  }

  .form {
    margin-top: 10px;
  }
</style>
