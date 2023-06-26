import { config } from './config.js'
import { OrderInfo } from './orderinfo.js'

export class OrderProcessor {
  constructor (websocket, feedbackProcessor, queueProcessor, statusProcessor, notificationProcessor) {
    this._websocket = websocket
    this._notificationProcessor = notificationProcessor
    this._feedbackProcessor = feedbackProcessor
    this._queueProcessor = queueProcessor
    this._statusProcessor = statusProcessor
    this._hideSuccessLabelAfterTimeoutVal = null
    this._successLabelDurationTimeout = config.hideSuccessMessageTimeout
    this._pollStatusMessagesTimeout = config.pollStatusMessagesTimeout
    this._pollStatusMessagesTimeoutId = null
    this._orderInfo = null
    this._scanStatusBar = document.getElementById('scan-status-bar')
  }

  init () {
    this._websocket.initOrderProcessing((data) => {
      this._processOrderMessage(data)
    },
    (error) => {
      this._notificationProcessor.updateSystemStatusMessage(error)
    })
  }

  reportIssueWithOrder () {
    this._feedbackProcessor.sendFeedback(this._orderInfo)
  }

  _processOrderMessage (message) {
    this._orderInfo = new OrderInfo(message)
    if (this._orderInfo != null) {
      this._statusProcessor.clearPollStatusMessagesInterval()

      if (this._pollStatusMessagesTimeoutId) {
        clearInterval(this._pollStatusMessagesTimeoutId)
      }

      this._queueProcessor.enqueueItem(this._orderInfo)
      this._renderOrderInfo(this._orderInfo)
      this._hideSuccessLabelAfterTimeout()

      this._pollStatusMessagesTimeoutId = setTimeout(() => { this._statusProcessor.pollStatusMessagesOnOrderEvent(this._orderInfo) }, this._pollStatusMessagesTimeout)
      this._statusProcessor.resetDisplayDefaultStatusTimeout()
    }
  }

  _renderOrderInfo (orderInfo) {
    this._scanStatusBar.style.background = '#7DD3A1'

    $('#default-scan-status').hide()
    $('#status-info').hide()
    $('#issue-reported').hide()
    $('#issue-not-reported').hide()
    $('#scan-status-bar').show()
    $('#order-info').show()
    $('#report-issue').show()
    $('#in-queue-text').show()
    $('#success-message').show()

    const labelContainer = document.querySelector('#label-container')
    while (labelContainer.firstChild) {
      labelContainer.removeChild(labelContainer.firstChild)
    }

    const transformedFields = orderInfo.transformed_fields

    let orderInfoInnerHtml = ''
    for (const field in transformedFields) {
      orderInfoInnerHtml += '<div>'
      orderInfoInnerHtml += '<label>'
      orderInfoInnerHtml += transformedFields[field]
      orderInfoInnerHtml += '</label>'
      orderInfoInnerHtml += '</div>'
    }

    $('#label-container').append(orderInfoInnerHtml)
  }

  _hideSuccessLabelAfterTimeout () {
    if (this._hideSuccessLabelAfterTimeoutVal) {
      clearTimeout(this._hideSuccessLabelAfterTimeoutVal)
    }

    this._hideSuccessLabelAfterTimeoutVal = setTimeout(() => {
      $('#success-message').hide()
    }, this._successLabelDurationTimeout)
  }
}
