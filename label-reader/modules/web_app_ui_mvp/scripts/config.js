export const config = {
  websocketVideostreamUrl: '/ws/vid_stream',
  websocketOrderInfoUrl: '/ws/order_info',
  websocketStatusUrl: '/ws/status',
  websocketFeedbackUrl: '/ws/feedback',
  websocketAdminControlUrl: '/ws/admin',
  websocketVideostreamPort: 7001,
  websocketOrderInfoPort: 7001,
  websocketStatusPort: 7001,
  websocketFeedbackPort: 7001,
  websocketAdminControlPort: 7001,
  websocketRetryTimeout: 5000,
  websocketMaxRetries: 300,
  checkWebsocketConnectionInterval: 1000,
  checkIsVideoLiveInterval: 2000,
  playAudioInterval: 3000,
  moveOrderToAudioQueueInterval: 1,
  pollStatusMesssagesOnStartUpInterval: 2000,
  pollStatusMesssagesOnOrderEventInterval: 2000,
  pollStatusMessagesTimeout: 5000,
  pollSystemStatusMessagesInterval: 10000,
  pollNotificationPanelUpdateInterval: 10,
  displayDefaultStatusTimeout: 5000,
  hideSuccessMessageTimeout: 2000,
  displayTextLowBoundingBoxesError: 'Turn the label to the front of the camera',
  displayTextOCRValidationError: 'Sorry, we can\'t read this label',
  displayTitleSystemError: 'System error',
  displayDescSystemError: 'Please contact IT for assistance.',
  displayTitleCameraError: 'camera not working',
  displayDescCameraError: 'Please contact IT for assistance',
  displayTitleAudioError: 'Browser can\'t play audio',
  displayDescAudioError: 'Please try opening the page on a different browser or contact IT for assistance.',
  displayTitleWebsocketError: 'Error connecting to system backend',
  displayDescWebsocketError: 'Attempting connection retry. No action required.'
}
