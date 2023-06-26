import { StatusInfo } from './statusinfo.js'
export class AudioProcessor {
  constructor (notificationProcessor) {
    this.context = null
    this.initAudioContext(notificationProcessor)
  }

  initAudioContext (notificationProcessor) {
    console.log('Initialize Audio context!')
    if (!window.AudioContext) {
      if (!window.webkitAudioContext) {
        console.error('Your browser does not support any AudioContext and cannot play back this audio.')
        return
      }

      window.AudioContext = window.webkitAudioContext
    }

    this.context = new AudioContext()

    if (this.context === null) {
      const currTs = new Date().getTime()
      const statusMessage = {
        is_cup_detected: null,
        is_error: true,
        error_code: 'SYSTEM',
        error_sub_type: 'NO_AUDIO_CONTEXT',
        correlation_id: null,
        timestamp: currTs
      }
      const statusInfo = new StatusInfo(statusMessage)
      notificationProcessor.updateSystemStatusMessage(statusInfo)
      console.error('Error: Audio context is null')
    }
  }

  resumeAudioContext () {
    if (this.context !== null) {
      if (this.context.state === 'suspended') {
        console.log('Resuming audio context')
        this.context.resume()
      }
    }
  }

  playByteArray (arrayBuffer, onEndedCallback) {
    if (this.context !== null) {
      this.context.decodeAudioData(arrayBuffer, (buffer) => {
        if (this.context.state === 'running') {
          this._play(buffer, onEndedCallback)
        } else if (this.context.state === 'suspended') {
          this.context.resume().then(() => {
            this._play(buffer, onEndedCallback)
          })
        }
      })
    }
  }

  _play (buffer, onEndedCallback) {
    const analyser = this.context.createAnalyser()

    const source = this.context.createBufferSource()
    source.buffer = buffer
    source.onended = () => {
      onEndedCallback()
    }
    source.connect(analyser)
    analyser.connect(this.context.destination)

    source.start(0)
  }
};
