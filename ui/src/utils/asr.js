import Recorder from 'js-audio-recorder'
import ReconnectingWebSocket from 'reconnecting-websocket'

class Asr {
  onopen = () => {}
  ontext = text => {}
  onerror = () => {}
  onclose = () => {}
  constructor() {
    this.recorder = new Recorder({
      sampleBits: 16,
      sampleRate: 16000,
      numChannels: 1,
    })

    this.fulltext = ''
  }

  connect() {
    this.wsurl = localStorage.getItem('asrurl')
    if (!this.wsurl) {
      return
    }
    this.ws = new ReconnectingWebSocket(this.wsurl)
    this.ws.addEventListener('open', () => {
      console.log('ASR服务连接成功')
      const request = {
        mode: 'offline',
        chunk_size: [5, 10, 5],
        is_speaking: false,
      }
      this.ws.send(JSON.stringify(request))
      this.onopen()
    })
    this.ws.addEventListener('message', e => {
      const data = JSON.parse(e.data)
      if (data.text) {
        this.fulltext += data.text
      }
      if (data.is_final) {
        this.fulltext = this.fulltext.replace(/<\|.*?\|>/g, '')
        this.ontext(this.fulltext)
        this.fulltext = ''
      }
    })
    this.ws.addEventListener('error', e => {
      console.log('ASR服务连接错误', e)
      this.onerror(e)
    })
    this.ws.addEventListener('close', () => {
      console.log('ASR服务连接关闭')
      this.onclose()
    })
  }

  isConnected() {
    return !!this.ws
  }

  getPermission() {
    return Recorder.getPermission()
  }

  start(success = () => {}, fail = () => {}) {
    this.recorder.start().then(
      () => {
        console.log('录音开始')
        success()
      },
      () => {
        console.log('录音开始失败')
        fail()
      },
    )
  }

  stop(callback = () => {}, send = false) {
    console.log('录音结束')
    if (send) {
      const sendFileInChunks = (blob, chunkSize = 1024) => {
        this.ws.send(JSON.stringify({ is_speaking: true }))
        let start = 0
        const totalChunks = Math.ceil(blob.size / chunkSize)
        for (let i = 0; i < totalChunks; i++) {
          const end = start + chunkSize
          const chunk = blob.slice(start, end)
          this.ws.send(chunk)
          start = end
        }
        this.ws.send(JSON.stringify({ is_speaking: false }))
      }
      this.recorder.stop()
      const blob = this.recorder.getWAVBlob()
      sendFileInChunks(blob)
    } else {
      this.recorder.stop()
    }
    callback()
  }

  getWAVBlob() {
    return this.recorder.getWAVBlob()
  }
}

const asr = new Asr()

export default asr
