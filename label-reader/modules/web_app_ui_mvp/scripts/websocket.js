import { config } from './config.js'
import { WebSocketClient } from './websocketclient.js'

export class Websocket {
  constructor () {
    this.root_url = 'ws://' + window.location.hostname + ':'
    this.videoStream_url = this.root_url + config.websocketVideostreamPort + config.websocketVideostreamUrl
    this.orderInfo_url = this.root_url + config.websocketOrderInfoPort + config.websocketOrderInfoUrl
    this.status_url = this.root_url + config.websocketStatusPort + config.websocketStatusUrl
    this.feedback_url = this.root_url + config.websocketFeedbackPort + config.websocketFeedbackUrl
    this.adminControl_url = this.root_url + config.websocketAdminControlPort + config.websocketAdminControlUrl

    this.videoStreamClient = null
    this.orderInfoClient = null
    this.statusClient = null
    this.feedbackClient = null
    this.adminControlClient = null
  }

  initVideoStream (onMessageCallback, onCloseStreamCallback, closeWSErrorCallback) {
    this.videoStreamClient = new WebSocketClient(closeWSErrorCallback, this.videoStream_url, (data) => {
      this._processData(onMessageCallback, data, true)
    }, 'arraybuffer', onCloseStreamCallback)
    this.videoStreamClient.init()
  }

  initOrderProcessing (onMessageCallback, closeWSErrorCallback) {
    this.orderInfoClient = new WebSocketClient(closeWSErrorCallback, this.orderInfo_url, (data) => {
      this._processData(onMessageCallback, data)
    })
    this.orderInfoClient.init()
  }

  initStatusProcessing (onMessageCallback, closeWSErrorCallback) {
    this.statusClient = new WebSocketClient(closeWSErrorCallback, this.status_url, (data) => {
      this._processData(onMessageCallback, data)
    })
    this.statusClient.init()
  }

  initAdminControl (onMessageCallback, closeWSErrorCallback) {
    this.adminControlClient = new WebSocketClient(closeWSErrorCallback, this.adminControl_url, (data) => {
      this._processData(onMessageCallback, data)
    })
    this.adminControlClient.init()
  }

  initFeedbackProcessing (onMessageCallback, closeWSErrorCallback) {
    this.feedbackClient = new WebSocketClient(closeWSErrorCallback, this.feedback_url, (data) => {
      this._processData(onMessageCallback, data)
    })
    this.feedbackClient.init()
  }

  _processData (onMessageCallback, data, decode = false) {
    try {
      if (data) {
        if (decode) {
          // eslint-disable-next-line no-undef
          onMessageCallback(MessagePack.decode(data))
        } else {
          onMessageCallback(JSON.parse(data))
        }
      }
    } catch (err) {
      console.log('Error while parsing response:' + err + 'data:' + data)
    }
  }

  sendAdminControlMessage (message) {
    if (this.adminControlClient) {
      this.adminControlClient.send(JSON.stringify(message))
    }
  }

  sendFeedbackMessage (message) {
    if (this.feedbackClient) {
      this.feedbackClient.send(JSON.stringify(message))
    }
  }
};
