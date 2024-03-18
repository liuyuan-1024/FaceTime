<script lang="ts" setup>
import {ElMessage} from 'element-plus'
import {onMounted, ref} from 'vue'
import {recordInformation2, signIn2} from '@/api/face'

// 开启摄像头
function startCamera() {
  navigator.mediaDevices
      .getUserMedia({video: true})
      .then(function (stream) {
        // 摄像头开启成功
        localVideo.value.srcObject = stream
        localVideo.value.play()
      })
      .catch(function (err) {
        /* 处理error */
        console.log(err)
      })
}

// 想要停止摄像头，调用这个函数
// function stopCamera() {
//   // 停止所有媒体流轨道
//   let stream = localVideo.value.srcObject
//   stream.getTracks().forEach((track: { stop: () => any }) => track.stop())
//   // 关闭媒体流
//   localVideo.value.srcObject = null
// }

onMounted(() => {
  startCamera()
})

let userId = ref<number>()
let userName = ref<string>()

// video标签的DOM
let localVideo = ref<any>()
let localCanvas = ref<any>()

function canvasImage(): string {
  const video = localVideo.value
  const canvas = localCanvas.value

  const ctx = canvas.getContext('2d')
  ctx.drawImage(video, 0, 0, canvas.width, canvas.height)
  // 将canvas上的图片转成base64编码
  return canvas.toDataURL('image/jpeg').split(',')[1]
}

function record_web() {
  if (!userId.value || !userName.value) {
    ElMessage.warning('请填写完整基本信息')
    return
  }

  const image = canvasImage()
  ElMessage.info('请稍等，正在录入信息')

  recordInformation2(userId.value, userName.value, image)
      .then((res) => {
        if (res) {
          ElMessage.success('录入信息成功')
        } else {
          ElMessage.warning('录入信息失败')
        }
      })
      .catch((err) => {
        ElMessage.error(err.message)
      })
}

function sign_web() {
  const image = canvasImage()
  ElMessage.info('请稍等，正在签到')

  signIn2(image)
      .then((res) => {
        if (res) {
          ElMessage.success('签到成功')
        } else {
          ElMessage.warning('签到失败')
        }
      })
      .catch((err) => {
        ElMessage.error(err.message)
      })
}
</script>

<template>
  <h1>FaceTime</h1>

  <div>
    <video id="localVideo" ref="localVideo"></video>
    <canvas id="localCanvas" ref="localCanvas"></canvas>
  </div>
  <div id="bar">
    <div>
      <input v-model="userId" placeholder="你的ID" type="number"/>
      <input v-model="userName" placeholder="你的姓名"/>
      <button @click="record_web()">录入信息</button>
    </div>

    <div>
      <button @click="sign_web()">考勤签到WEB</button>
    </div>
  </div>
</template>

<style scoped>
#localCanvas {
  width: 640px;
  height: 480px;
  background-color: aquamarine;
}

input {
  width: 200px;
  height: 35px;
}

#bar {
  display: grid;
  grid-template-columns: repeat(2, 800px);
}
</style>
