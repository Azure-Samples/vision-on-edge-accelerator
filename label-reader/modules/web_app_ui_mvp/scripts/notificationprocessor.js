import { config } from './config.js'
import { Notification } from './notification.js'
import { StatusInfo } from './statusinfo.js'
export class NotificationProcessor {
  constructor (websocket) {
    this._systemStatusMessages = {}
    this._notificationsForDisplay = {}
    this._websocket = websocket
    this._pollSystemStatusMessagesInterval = config.pollSystemStatusMessagesInterval
    this._pollSystemStatusMessagesIntervalId = null
    this._pollNotificationPanelUpdateInterval = config.pollNotificationPanelUpdateInterval
    this._pollNotificationPanelUpdateIntervalId = null
    this._checkNotificationsOlderThanMilliSec = 3000
    this._errorTitleSystem = config.displayTitleSystemError
    this._errorDescSystem = config.displayDescSystemError
    this._errorTitleCamera = config.displayTitleCameraError
    this._errorDescCamera = config.displayDescCameraError
    this._errorTitleAudio = config.displayTitleAudioError
    this._errorDescAudio = config.displayDescAudioError
    this._errorTitleWebsocket = config.displayTitleWebsocketError
    this._errorDescWebsocket = config.displayDescWebsocketError
  }

  init () {
    this._websocket.initStatusProcessing((data) => {
      this.updateSystemStatusMessage(data)
    },
    (error) => {
      this.updateSystemStatusMessage(error)
    })

    this._pollSystemStatusMessages()
    this._pollNotificationPanelUpdate()
  }

  updateSystemStatusMessage (message) {
    const errorCode = message.error_code
    if (errorCode === 'SYSTEM') {
      const systemStatusMessage = new StatusInfo(message)
      this._systemStatusMessages[systemStatusMessage.error_sub_type] = { ...systemStatusMessage, isDisplayed: false }
    }
  }

  _pollSystemStatusMessages () {
    this._pollSystemStatusMessagesIntervalId = setInterval(() => {
      this._processSystemStatusMessages()
    }, this._pollSystemStatusMessagesInterval)
  }

  _processSystemStatusMessages () {
    $.each(this._systemStatusMessages, (key, value) => {
      const _existingNotification = this._notificationsForDisplay[key]
      if (!_existingNotification || this._isNewNotification(value, _existingNotification)) {
        const notification = this._getNotification(value)
        this._notificationsForDisplay[notification.id] = { ...notification, isDisplayed: false }
      }
      delete this._systemStatusMessages[key]
    })
  }

  _isNewNotification (newNotification, existingNotification) {
    const currTimestamp = new Date().getTime()
    if (newNotification.timestamp > existingNotification.timestamp && (currTimestamp - newNotification.timestamp) < this._checkNotificationsOlderThanMilliSec) {
      return true
    }
    return false
  }

  _pollNotificationPanelUpdate () {
    this._pollNotificationPanelUpdateIntervalId = setInterval(() => {
      this._updateNotificationPanel()
    }, this._pollNotificationPanelUpdateInterval)
  }

  _updateNotificationPanel () {
    this._updateNotificationBellIcon()
    $.each(this._notificationsForDisplay, (key, value) => {
      if (!value.isDisplayed) {
        this._displayNotification(value)
      }
    })
  }

  _updateNotificationBellIcon () {
    const unreadNotifications = Object.fromEntries(Object.entries(this._notificationsForDisplay).filter(([key, value]) => !value.isDisplayed))
    if (Object.keys(unreadNotifications).length > 0) {
      $('#notification-icon-red-dot').show()
      $('#notifications-list').show()
      $('#no-notifications').hide()
    } else {
      $('#notification-icon-red-dot').hide()
      $('#notifications-list').hide()
      $('#no-notifications').show()
    }
  }

  _displayNotification (notificationItem) {
    const notificationTimestamp = new Date(notificationItem.timestamp).toLocaleTimeString([], { day: 'numeric', month: 'long', year: 'numeric', hour: '2-digit', minute: '2-digit' })

    const id = `#${notificationItem.id}`
    if ($('#notifications-list').find(id).length === 0) {
      const notificationHtmlTemplate = `
      <div id="${notificationItem.id}" class="notification-item">
        <div class="notification-item-container">
          <div class="notification-item-logo">
            <svg width="50%" viewBox="-18 -18 36 36" fill="none" xmlns="http://www.w3.org/2000/svg">
              <circle r="50%" fill="#EC5252"/>
              <path transform="translate(-9,-9)" d="M8.01884 0.243919C8.95388 -0.253934 10.1212 0.0353506 10.6948 0.883826L10.7692 1.00297L17.7466 13.1125C17.9128 13.401 18 13.7253 18 14.055C18 15.0844 17.168 15.9271 16.1152 15.9955L15.9766 16H2.02374C1.68083 16 1.34356 15.9162 1.04357 15.7565C0.108474 15.2588 -0.255769 14.1542 0.188072 13.2366L0.253627 13.1127L7.22911 1.00317C7.41303 0.683873 7.68671 0.420763 8.01884 0.243919ZM16.5666 13.7408L9.58921 1.63125C9.40873 1.31802 8.99827 1.20474 8.67242 1.37823C8.58939 1.42244 8.51732 1.48283 8.46061 1.55516L8.40918 1.63132L1.4337 13.7409C1.25326 14.0541 1.37115 14.4487 1.69702 14.6222C1.77201 14.6621 1.854 14.6878 1.93853 14.6981L2.02374 14.7033H15.9766C16.3491 14.7033 16.6511 14.413 16.6511 14.055C16.6511 13.9725 16.6347 13.8911 16.6032 13.815L16.5666 13.7408L9.58921 1.63125L16.5666 13.7408ZM9 11.6717C9.49599 11.6717 9.89807 12.0583 9.89807 12.5351C9.89807 13.0118 9.49599 13.3984 9 13.3984C8.50401 13.3984 8.10193 13.0118 8.10193 12.5351C8.10193 12.0583 8.50401 11.6717 9 11.6717ZM8.99622 5.18637C9.33767 5.18611 9.62006 5.4298 9.66499 5.74622L9.67122 5.83419L9.67446 9.72564C9.67475 10.0837 9.37303 10.3742 9.00054 10.3745C8.65909 10.3748 8.3767 10.1311 8.33178 9.81465L8.32555 9.72668L8.32231 5.83523C8.32201 5.47716 8.62373 5.18665 8.99622 5.18637Z" fill="#EDEDED"/>
            </svg>
          </div>
          <div class="notification-item-content">
            <div class="issue-detected">Issue detected</div>
            <div class="notification-item-title">${notificationItem.title}</div>
            <div id="notification-item-timestamp" class="notification-item-timestamp">${notificationItem.timestamp}</div>
            <div class="notification-item-desc">${notificationItem.description}</div>
          </div>
        </div>
        <div class="notification-dismiss-button-container">
          <button class="notification-dismiss-button">忽略</button>
        </div>
      </div>`

      $('#notifications-list').append(notificationHtmlTemplate)

      this._bindDismissNotification()
    } else {
      $(`#${notificationItem.id} #notification-item-timestamp`).text(notificationTimestamp)
    }
  }

  _bindDismissNotification () {
    $('.notification-dismiss-button').click((event) => {
      event.preventDefault()
      const id = $(event.target).parent().parent().attr('id')
      this._notificationsForDisplay[id].isDisplayed = true
      $(event.target).parent().parent().remove()
    })
  }

  _getNotification (systemStatusMessage) {
    let notificationId = ''
    let notificationTitle = ''
    let notificationDesc = ''
    let notificationTs = ''
    if (systemStatusMessage) {
      switch (systemStatusMessage.error_sub_type) {
        case 'EDGE_MODEL_ERROR':
        case 'OCR_ERROR':
        case 'TTS_ERROR':
          notificationId = 'system-error'
          notificationTitle = this._errorTitleSystem
          notificationDesc = this._errorDescSystem
          notificationTs = systemStatusMessage.timestamp
          break
        case 'NO_VIDEO_FRAME':
          notificationId = 'camera-error'
          notificationTitle = this._errorTitleCamera
          notificationDesc = this._errorDescCamera
          notificationTs = systemStatusMessage.timestamp
          break
        case 'NO_AUDIO_CONTEXT':
          notificationId = 'audiocontext-error'
          notificationTitle = this._errorTitleAudio
          notificationDesc = this._errorDescAudio
          notificationTs = systemStatusMessage.timestamp
          break
        case 'WEBSOCKET_ERROR':
          notificationId = 'websocket-error'
          notificationTitle = this._errorTitleWebsocket
          notificationDesc = this._errorDescWebsocket
          notificationTs = systemStatusMessage.timestamp
          break
      }
    }
    const notification = new Notification(notificationId, notificationTitle, notificationDesc, notificationTs)
    return notification
  }

  toggleNotificationPanel () {
    $('#notification-panel').toggle('slide')
  }
}
