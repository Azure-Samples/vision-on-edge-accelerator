import { Websocket } from './websocket.js'
import { FrameProcessor } from './frameprocessor.js'
import { AudioProcessor } from './audioprocessor.js'
import { QueueProcessor } from './queueprocessor.js'
import { OrderProcessor } from './orderprocessor.js'
import { StatusProcessor } from './statusprocessor.js'
import { FeedbackProcessor } from './feedbackprocessor.js'
import { NotificationProcessor } from './notificationprocessor.js'
import { AdminControl } from './admincontrol.js'

(() => {
  const webSocket = new Websocket()
  const notificationProcessor = new NotificationProcessor(webSocket)
  const audioProcessor = new AudioProcessor(notificationProcessor)
  const queueProcessor = new QueueProcessor(audioProcessor)
  const statusProcessor = new StatusProcessor(webSocket, notificationProcessor)
  const feedbackProcessor = new FeedbackProcessor(webSocket, notificationProcessor)
  const frameProcessor = new FrameProcessor(webSocket, notificationProcessor)
  const orderProcessor = new OrderProcessor(webSocket, feedbackProcessor, queueProcessor, statusProcessor, notificationProcessor)
  const adminControl = new AdminControl(webSocket, frameProcessor, notificationProcessor)

  $(document).on('change', '#live-feed-switch', function (e) {
    const isLiveFeedOn = e.target.checked
    adminControl.sendAdminControlRequest(isLiveFeedOn)
  })

  $('#welcome-modal').modal('show')

  $('#ok-button').click(function () {
    audioProcessor.resumeAudioContext()
  })

  $('#live-feed-settings-button').click(function () {
    $('#live-feed-settings-button').addClass('links-selected')
    $('#live-feed-button').removeClass('links-selected')
    adminControl.showAdminControlDialog()
  })

  $('#live-feed-button').click(function () {
    $('#live-feed-settings-button').removeClass('links-selected')
    $('#live-feed-button').addClass('links-selected')
  })

  $('#report-issue-button').click(function () {
    orderProcessor.reportIssueWithOrder()
  })

  $('#notification-button').click(function () {
    notificationProcessor.toggleNotificationPanel()
  })

  $('#notification-close-button').click(function () {
    notificationProcessor.toggleNotificationPanel()
  })

  frameProcessor.init()
  queueProcessor.init()
  orderProcessor.init()
  statusProcessor.init()
  feedbackProcessor.init()
  notificationProcessor.init()
  adminControl.init()
})()
