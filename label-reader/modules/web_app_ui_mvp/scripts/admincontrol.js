import { AdminControlMessage } from './admincontrolmessage.js'
import { config } from './config.js'
import { StatusInfo } from './statusinfo.js'

export class AdminControl {
  constructor (websocket, frameProcessor, notificationProcessor) {
    this._websocketconn = websocket
    this._frameProcessor = frameProcessor
    this._notificationProcessor = notificationProcessor
  }

  init () {
    this._websocketconn.initAdminControl((data) => {
      this._processAdminControlResponseMessage(data)
    },
    (error) => {
      this._notificationProcessor.updateSystemStatusMessage(error)
    })
    this._disableLiveFeedSwitch(false)
  }

  sendAdminControlRequest (isLiveFeedOn) {
    const request = {
      command: (isLiveFeedOn) ? 'start' : 'stop',
      type: 'request',
      status: 'initiated'
    }
    const adminControlMessage = new AdminControlMessage(request)
    this._websocketconn.sendAdminControlMessage(adminControlMessage)
    this._disableLiveFeedSwitch(true)
    this._changeToggleSwitchMessage(isLiveFeedOn, false)
    this._frameProcessor.setLiveFeedSwitchState(isLiveFeedOn)
  }

  _processAdminControlResponseMessage (message) {
    this._disableLiveFeedSwitch(false)
    try {
      const adminControlMessage = new AdminControlMessage(message)
      if (adminControlMessage.status === 'success') {
        const isLiveFeedOn = adminControlMessage.command === 'start'
        this._changeToggleSwitchMessage(isLiveFeedOn, true)
      } else {
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
        this._notificationProcessor.updateSystemStatusMessage(errorStatus)
      }
    } catch (err) {
      console.log('Error while receiving admin control response:' + err)
    }
  }

  _disableLiveFeedSwitch (flag) {
    $('#live-feed-switch').prop('disabled', flag)
  }

  _disableCloseButton (flag) {
    $('#admin-control-close-button').prop('disabled', flag)
  }

  _changeToggleSwitchMessage (action, isComplete) {
    if (!isComplete) {
      if (action) {
        $('#live-feed-switch-label').text('Starting up')
      } else {
        $('#live-feed-switch-label').text('Shutting down')
      }
    } else {
      if (action) {
        $('#live-feed-switch-label').text('Ready to use')
      } else {
        $('#live-feed-switch-label').text('Shut down complete')
      }
    }
  }

  _setPropertiesForToggleLiveFeedSwitch () {
    const isLiveFeedOn = this._checkForLiveFeed()
    this._disableLiveFeedSwitch(false)
    $('#live-feed-switch').prop('checked', isLiveFeedOn)
    if (isLiveFeedOn) {
      $('#live-feed-switch-label').text('Live Feed On')
    } else {
      $('#live-feed-switch-label').text('Live Feed Off')
    }
  }

  _checkForLiveFeed () {
    const currTs = new Date().getTime()
    if (currTs - this._frameProcessor.getLastFrameTs() > config.checkIsVideoLiveInterval) {
      return false
    } else {
      return true
    }
  }

  showAdminControlDialog () {
    this._setPropertiesForToggleLiveFeedSwitch()
    $('#live-feed-settings-modal').modal('show')

    $('#live-feed-settings-modal').on('hidden.bs.modal', function () {
      $('#live-feed-settings-button').removeClass('links-selected')
      $('#live-feed-button').addClass('links-selected')
    })
  }
}
