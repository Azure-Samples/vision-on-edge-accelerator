import { config } from './config.js'
import { StatusInfo } from './statusinfo.js'

export class StatusProcessor {
  constructor (websocket, notificationProcessor) {
    this._websocket = websocket
    this._notificationProcessor = notificationProcessor
    this._statusMessage = null
    this._displayDefaultStatusTimeout = config.displayDefaultStatusTimeout
    this._displayDefaultStatusTimeoutId = null
    this._pollStatusMesssagesOnStartUpInterval = config.pollStatusMesssagesOnStartUpInterval
    this._pollStatusMesssagesOnStartUpIntervalId = null
    this._pollStatusMessagesOnOrderEventInterval = config.pollStatusMesssagesOnOrderEventInterval
    this._pollStatusMessagesOnOrderEventIntervalId = null
    this._checkStatusMessageOlderThanMilliSec = 3000
    this._errorLowBoundingBoxes = config.displayTextLowBoundingBoxesError
    this._errorOCRValidation = config.displayTextOCRValidationError
    this._statusColorLowBoundingBoxes = '#FFBB10'
    this._statusColorOCRValidation = '#EC5252'
    this._scanStatusBar = document.getElementById('scan-status-bar')
  }

  init () {
    this._websocket.initStatusProcessing((data) => {
      this._updateStatusMessage(data)
    },
    (error) => {
      this._notificationProcessor.updateSystemStatusMessage(error)
    })

    this._pollStatusMesssagesOnStartUp()
  }

  _updateStatusMessage (message) {
    const errorCode = message.error_code
    if (errorCode === 'LABEL_EXTRACTION') {
      this._statusMessage = new StatusInfo(message)
    }
  }

  _pollStatusMesssagesOnStartUp () {
    this._pollStatusMesssagesOnStartUpIntervalId = setInterval(() => {
      this._showStatusMessage()
    }, this._pollStatusMesssagesOnStartUpInterval)
  }

  pollStatusMessagesOnOrderEvent (orderInfo) {
    if (orderInfo) {
      this._pollStatusMessagesOnOrderEventIntervalId = setInterval(() => {
        this._renderStatusMessageOnOrderEvent(orderInfo)
      }, this._pollStatusMessagesOnOrderEventInterval)
    }
  }

  clearPollStatusMessagesInterval () {
    if (this._pollStatusMesssagesOnStartUpIntervalId) {
      clearInterval(this._pollStatusMesssagesOnStartUpIntervalId)
    }

    if (this._pollStatusMessagesOnOrderEventIntervalId) {
      clearInterval(this._pollStatusMessagesOnOrderEventIntervalId)
    }
  }

  _renderStatusMessageOnOrderEvent (orderInfo) {
    if (this._statusMessage) {
      if (this._okToShowStatusMessage(orderInfo, this._statusMessage)) {
        this._showStatusMessage()
      }
    }
  }

  _okToShowStatusMessage (orderInfo, statusInfo) {
    const currTimestamp = new Date().getTime()
    if (statusInfo.timestamp > orderInfo.timestamp &&
            (currTimestamp - statusInfo.timestamp) < this._checkStatusMessageOlderThanMilliSec) {
      return true
    }
    return false
  }

  _showStatusMessage () {
    if (this._statusMessage !== null) {
      const errorMessage = this._getErrorMessage()

      if (errorMessage === this._errorLowBoundingBoxes) {
        this._scanStatusBar.style.background = this._statusColorLowBoundingBoxes
      } else if (errorMessage === this._errorOCRValidation) {
        this._scanStatusBar.style.background = this._statusColorOCRValidation
      }

      $('#default-scan-status').hide()
      $('#order-info').hide()
      $('#success-message').hide()
      $('#scan-status-bar').show()
      $('#status-info').show()
      $('#status-message').text(errorMessage)
      this._statusMessage = null

      this.resetDisplayDefaultStatusTimeout()
    }
  }

  _getErrorMessage () {
    let errorMessage = ''
    if (this._statusMessage.is_error) {
      switch (this._statusMessage.error_sub_type) {
        case 'LOW_BB':
          errorMessage = this._errorLowBoundingBoxes
          break
        case 'FIELD_MISSING':
        case 'LOW_FIELD_CONFIDENCE':
          errorMessage = this._errorOCRValidation
          break
        default:
          errorMessage = 'Unknown error'
          break
      }
    }
    return errorMessage
  }

  resetDisplayDefaultStatusTimeout () {
    if (this._displayDefaultStatusTimeoutId) {
      clearTimeout(this._displayDefaultStatusTimeoutId)
    }
    this._displayDefaultStatusTimeoutId = setTimeout(this._renderDefaultStatus, this._displayDefaultStatusTimeout)
  }

  _renderDefaultStatus () {
    $('#default-scan-status').show()
    $('#scan-status-bar').hide()
    $('#status-info').hide()
    $('#order-info').hide()
  }
}
