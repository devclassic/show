<template>
  <div class="box">
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
        <el-menu-item index="/health/analysis">数据分析</el-menu-item>
        <el-menu-item index="/health/triage">分诊导诊</el-menu-item>
        <el-menu-item index="/health/assist">辅助诊疗</el-menu-item>
        <el-menu-item index="/health/check">内涵质控</el-menu-item>
        <el-menu-item index="/health/image">医学影像</el-menu-item>
        <el-menu-item index="/health/heart">心脏超声</el-menu-item>
      </el-sub-menu>
    </el-menu>
    <div class="main">
      <RouterView />
    </div>
  </div>
</template>

<script setup>
  import { useRoute } from 'vue-router'

  const route = useRoute()
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
