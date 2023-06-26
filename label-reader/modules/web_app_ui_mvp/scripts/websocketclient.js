import { config } from './config.js'
import { StatusInfo } from './statusinfo.js'

const CHECK_WEBSOCKET_CONNECTION_INTERVAL = config.checkWebsocketConnectionInterval
const RETRY_TIMEOUT = config.websocketRetryTimeout
const MAX_RETRIES = config.websocketMaxRetries

export class WebSocketClient {
  constructor (closeWSErrorCallback, url, onMessageCallback, binaryType = 'blob', closeStreamCallback, numOfRetries = 0) {
    this._closeWSErrorCallback = closeWSErrorCallback
    this._url = url
    this._onMessageCallback = onMessageCallback
    this._binaryType = binaryType
    this._closeStreamCallback = closeStreamCallback
    this._numOfRetries = numOfRetries
    this._client = null
    this._checkConnectionIntervalId = null
  }

  init () {
    console.log('Creating websocket for url: ' + this._url)
    try {
      this._client = new WebSocket(this._url)
      this._client.binaryType = this._binaryType
      this._addEventHandlers()
      this._checkConnectionIntervalId = setInterval(this._checkConnection.bind(this),
        CHECK_WEBSOCKET_CONNECTION_INTERVAL)
    } catch (err) {
      console.log('Error while creating websocket ' + err.message)
    }
  }

  _addEventHandlers () {
    this._client.addEventListener('open', () => {
      console.log('Websocket open event ' + this._url)
    })

    this._client.addEventListener('close', (event) => {
      console.log('Websocket close event from ' + this._url + ', reason :' + event.reason + ', code: ' + event.code)
      this._client = null

      if (this._closeStreamCallback) {
        this._closeStreamCallback()
      }
      setTimeout(this.init.bind(this), RETRY_TIMEOUT)
    })

    this._client.addEventListener('error', (err) => {
      console.log('Websocket error event: ' + err.message + ', error code = ' + err.code + ', error reason = ' + err.reason)
    })

    this._client.addEventListener('message', (event) => {
      if (event?.data && this._onMessageCallback) {
        this._onMessageCallback(event.data)
      }
    })
  }

  _checkConnection () {
    if (this._client && this._client.readyState === WebSocket.CONNECTING) {
      console.log('Retrying connecting to websocket: ' + this._url)
      ++this._numOfRetries
      if (this._numOfRetries > MAX_RETRIES) {
        console.log('Max retries reached, closing websocket')
        this._client.close()
        clearInterval(this._checkConnectionIntervalId)
        this._numOfRetries = 0

        const currTs = new Date().getTime()
        const statusMessage = {
          is_cup_detected: null,
          is_error: true,
          error_code: 'SYSTEM',
          error_sub_type: 'WEBSOCKET_ERROR',
          correlation_id: null,
          timestamp: currTs
        }
        const errorStatus = new StatusInfo(statusMessage)
        this._closeWSErrorCallback(errorStatus)
      }
    }
  }

  send (data) {
    try {
      if (data) {
        console.log('Sending data for websocket: ' + this._url)
        this._client.send(data)
      }
    } catch (err) {
      console.log('Error while sending data for socket: ' + this._url + ', error:' + err)
    }
  }
}
