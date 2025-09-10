<template>
  <div class="title">多人对话</div>
  <div class="buttons">
    <el-button type="primary" @click="record">{{ state.btnRecordText }}</el-button>
    <el-button type="primary" @click="clean">清空内容</el-button>
    <span class="status">{{ state.status }}</span>
  </div>
  <div class="content">
    <div v-for="item in state.stts">
      <span style="color: red">说话人{{ item.spk }}：</span>
      {{ item.text }}
    </div>
  </div>
  <div class="buttons">
    <el-form label-width="auto">
      <el-form-item label="生成类型">
        <el-select v-model="state.type" placeholder="生成类型" @change="typeChange">
          <el-option label="请选择" value="请选择" />
          <el-option label="病例生成" value="病例生成" />
          <el-option label="问询笔录" value="问询笔录" />
          <el-option label="自定义" value="自定义" />
        </el-select>
      </el-form-item>
      <el-form-item label="提示词">
        <el-input
          v-model="state.prompt"
          :rows="5"
          type="textarea"
          placeholder="请输入多人对话生成内容提示词，对话内容为<对话>" />
      </el-form-item>
    </el-form>
    <div>
      <el-button type="primary" :loading="state.loading" @click="generate">对话内容生成</el-button>
    </div>
  </div>
  <div v-if="state.result" v-html="state.result" class="result"></div>
</template>

<script setup>
  import { reactive } from 'vue'
  import markdownit from 'markdown-it'
  import asr from '../../../utils/asr'
  import http from '../../../utils/http'
  import { format } from 'date-fns'

  const state = reactive({
    btnRecordText: '开始收音',
    status: '',
    type: '请选择',
    prompt: '',
    stts: [],
    result: '',
    loading: false,
  })

  const md = markdownit()

  function typeChange() {
    switch (state.type) {
      case '请选择':
        state.prompt = ''
        ElMessage.error('请选择生成类型')
        break
      case '病例生成':
        state.prompt = '<对话>为患者和医生的对话，根据<对话>生成一份完成的病例'
        break
      case '问询笔录':
        state.prompt = `<对话>为问询对话。
<模板>
问：
答：
</模板>
<模板>为问询笔录模板。
请根据<对话>内容，根据<模板>生成一份问询笔录。
你是一名公安机关反诈中心专职法制员，只准许引用<对话>里出现过的信息，禁止脑补、禁止推理、禁止添加对话未提及的任何情节。
现在时间为${format(new Date(), 'yyyy-MM-dd HH:mm:ss')}。
如果<对话>中没有<模板>的内容则留空。
问题主要有：
问：我们是青山区公安分局刑侦大队的民警（出示工作证件），现依法对你询问，根据我国法律相关规定，你应如实回答，歪曲和捏造事实将负法律责任。对与本案无关的问题，你有拒绝回答的权利，你听清楚了吗？ 
问：这是《证人诉讼权利义务告知书》你看一下在上面签字？（给你阅读，你如果不识字，我们可以给你宣读？）
问：你的个人信息？ （个人情况）
问：讲一下被骗的具体经过？（讲一下事情的详细经过）
问：讲一下你的被骗金额？
问：讲一下你使用的社交软件情况
问：讲一下你银行账户的情况？（你转账使用的银行账户）
问：讲一下对方的情况？
问：讲一下你按照对方要求进行转账的操作？
问：你是否可以提供相关的转账记录和聊天记录？ 
问：你在社区看没看到过反诈宣传？  
问：你还有什么要补充的？ 
问：以上讲的是否属实？
围绕着问题根据<对话>生成<模板>样式的问询笔录,未涉及到的问题不要出现在问询笔录里。
问询笔录中所有的数字使用阿拉伯数字表示。
生成的问询笔录的问和答尽可能使用书面用语。
`
        break
      case '自定义':
        state.prompt = ''
        break
    }
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
        state.btnRecordText = '开始收音'
        isRecoding = false
        state.status = '正在处理...'
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
        state.stts = res.data.data[0].sentence_info
        state.status = ''
      })
    }
  }

  function clean() {
    state.status = ''
    state.prompt = ''
    state.type = '请选择'
    state.stts = []
  }

  async function generate() {
    if (state.type == '请选择') {
      ElMessage.error('请选择生成类型')
      return
    }
    if (state.prompt == '') {
      ElMessage.error('请输入提示词')
      return
    }
    state.loading = true
    let temp = '<对话>\n'
    for (const item of state.stts) {
      temp += `说话人${item.spk}：${item.text}\n`
    }
    temp += '</对话>\n'
    const prompt = temp + state.prompt
    const res = await http.post('/api/asrg', { prompt })
    state.result = md.render(res.data.data.replace(/<think>[\s\S]*?<\/think>/g, ''))
    state.loading = false
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
    height: 200px;
    overflow: auto;
  }

  .result {
    border: 1px solid #cccccc;
    padding: 10px;
    margin-top: 10px;
  }
</style>
