import { Feedback } from './feedback.js'
export class FeedbackProcessor {
  constructor (websocket, notificationProcessor) {
    this._websocketconn = websocket
    this._notificationProcessor = notificationProcessor
  }

  init () {
    this._websocketconn.initFeedbackProcessing((data) => {
      this._processFeedbackAcknowledgementMessage(data)
    },
    (error) => {
      this._notificationProcessor.updateSystemStatusMessage(error)
    })
  }

  sendFeedback (orderInfo) {
    const feedbackMessage = new Feedback(orderInfo)
    this._websocketconn.sendFeedbackMessage(feedbackMessage)
  }

  _processFeedbackAcknowledgementMessage (message) {
    if (message.outcome === 'success') {
      $('#report-issue').hide()
      $('#issue-not-reported').hide()
      $('#issue-reported').show()
    } else {
      $('#report-issue').hide()
      $('#issue-reported').hide()
      $('#issue-not-reported').show()
    }
  }
}
