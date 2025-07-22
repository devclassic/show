<template>
  <div class="box">
    <el-dialog v-model="state.isOpenSettings" title="设置" width="500" draggable>
      <el-form label-width="auto">
        <el-form-item label="模式">
          <el-select v-model="state.sessings.mode" placeholder="请选择模式">
            <el-option label="线上模式" value="online" />
            <el-option label="本地模式" value="offline" />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button type="primary" @click="okSettings">确定</el-button>
      </template>
    </el-dialog>

    <el-menu :default-active="route.path" :router="true" mode="horizontal" menu-trigger="click">
      <el-menu-item index="/">首页</el-menu-item>
      <el-sub-menu index="/voice">
        <template #title>智能语音</template>
        <el-menu-item index="/voice/asr">语音识别</el-menu-item>
        <el-menu-item index="/voice/multi">多人对话</el-menu-item>
        <el-menu-item index="/voice/form">表单填写</el-menu-item>
      </el-sub-menu>
      <el-sub-menu index="/health">
        <template #title>医疗相关</template>
        <el-menu-item index="/health/triage">分诊导诊</el-menu-item>
        <el-menu-item index="/health/assist">辅助诊疗</el-menu-item>
        <el-menu-item index="/health/check">内涵质控</el-menu-item>
        <el-menu-item index="/health/image">医学影像</el-menu-item>
      </el-sub-menu>
      <el-menu-item index="" @click="openSettings">设置</el-menu-item>
    </el-menu>
    <div class="main">
      <RouterView />
    </div>
  </div>
</template>

<script setup>
  import { reactive, onMounted } from 'vue'
  import { useRoute } from 'vue-router'
  import asr from './utils/asr'

  const state = reactive({
    isOpenSettings: false,
    sessings: {
      mode: 'offline',
    },
  })

  const route = useRoute()

  onMounted(() => {
    const aurl = localStorage.getItem('asrurl')
    if (aurl) {
      state.sessings.mode = aurl === 'ws://localhost:10095' ? 'offline' : 'online'
    } else {
      state.sessings.mode = 'offline'
    }
    okSettings()
  })

  const openSettings = () => {
    state.isOpenSettings = true
  }

  const okSettings = () => {
    let asrurl = 'ws://localhost:10095'
    if (state.sessings.mode == 'online') {
      asrurl = 'wss://asr.epoint.ink'
    }
    localStorage.setItem('asrurl', asrurl)
    asr.connect()
    state.isOpenSettings = false
    ElMessage.success('设置成功')
  }
</script>

<style>
  * {
    box-sizing: border-box;
  }

  body {
    margin: 0;
    background-color: #f5f5f5;
  }

  .box {
    width: 1024px;
    margin: 10px auto 10px;
    border: 1px solid #cccccc;
    background-color: #ffffff;
  }

  .main {
    padding: 20px;
    min-height: calc(100vh - 20px - 60px - 5px);
    position: relative;
  }
</style>
