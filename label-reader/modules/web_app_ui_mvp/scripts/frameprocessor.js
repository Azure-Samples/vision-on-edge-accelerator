import { config } from './config.js'
import { StatusInfo } from './statusinfo.js'

export class FrameProcessor {
  constructor (websocket, notificationProcessor) {
    this._websocketconn = websocket
    this._notificationProcessor = notificationProcessor
    this._lastFrameTs = null
    this._checkIsVideoLiveInterval = config.checkIsVideoLiveInterval
    this._checkLastFrameOlderThanMilliSec = 2000
    this._chunkSize = 0x8000
    this._videoFeed = document.getElementById('video-feed')
    this._liveFeedState = false
  }

  init () {
    this._websocketconn.initVideoStream((data) => {
      this._processVideoStreamMessage(data)
    }, () => { this._showBlankScreen() },
    (error) => {
      this._notificationProcessor.updateSystemStatusMessage(error)
    })

    this._checkVideoAtInterval()
  }

  getLastFrameTs () {
    return this._lastFrameTs
  }

  setLiveFeedSwitchState (flag) {
    this._liveFeedState = flag
  }

  _showBlankScreen () {
    $('#video-feed').attr('src', 'images/blank_screen.png')
    $('#live-text').hide()
  }

  _checkVideoAtInterval () {
    setInterval(() => { this._checkIsVideoLive() }, this._checkIsVideoLiveInterval)
  }

  _checkIsVideoLive () {
    const currTs = new Date().getTime()
    if (this._lastFrameTs === null || currTs - this._lastFrameTs > this._checkLastFrameOlderThanMilliSec) {
      const statusMessage = {
        is_cup_detected: null,
        is_error: true,
        error_code: 'SYSTEM',
        error_sub_type: 'NO_VIDEO_FRAME',
        correlation_id: null,
        timestamp: currTs
      }
      const statusInfo = new StatusInfo(statusMessage)
      if (this._liveFeedState) {
        this._notificationProcessor.updateSystemStatusMessage(statusInfo)
      }
      console.log('No camera frame received in the last ' + this._checkLastFrameOlderThanMilliSec / 1000 + ' seconds')
      this._showBlankScreen()
    }
  }

  _renderLiveVideo (videoFrame) {
    this._videoFeed.src = videoFrame
    $('#live-text').show()
  }

  // Good explanation regarding this
  // https://stackoverflow.com/questions/12710001/how-to-convert-uint8-array-to-base64-encoded-string
  _uint8ToString (u8a) {
    const c = []
    for (let i = 0; i < u8a.length; i += this._chunkSize) {
      c.push(String.fromCharCode.apply(null, u8a.subarray(i, i + this._chunkSize)))
    }
    return c.join('')
  }

  _processVideoStreamMessage (message) {
    const frame = btoa(this._uint8ToString(message.raw_frame))
    this._renderLiveVideo(`data:image/jpeg;base64,${frame}`)
    this._lastFrameTs = new Date().getTime()
  }
};
