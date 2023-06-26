import { config } from './config.js'
import { Queue } from './queue.js'

export class QueueProcessor {
  constructor (audioProcessor) {
    this._audioProcessor = audioProcessor
    this._rawQueue = new Queue()
    this._playingQueue = new Queue()
    this._playAudioIntervalId = null
    this._moveToAudioQueueIntervalId = null
    this._playAudioInterval = config.playAudioInterval
    this._moveToAudioQueueInterval = config.moveOrderToAudioQueueInterval
    this._removedQueueItem = null
  }

  init () {
    this._moveToAudioQueueIntervalId = setInterval(() => { this._moveToAudioQueue() }, this._moveToAudioQueueInterval)
    this._processQueueItems()
  }

  enqueueItem (orderInfo) {
    if (orderInfo) {
      this._rawQueue.enqueue(orderInfo)
    }
  }

  _processQueueItems () {
    this._playAudioIntervalId = setInterval(() => { this._showPlayingOrderDetails() }, this._playAudioInterval)
  }

  _moveToAudioQueue () {
    if (this._rawQueue.length() > 0 && $('.queue-item').length < 4) {
      const orderInfo = this._rawQueue.dequeue()
      this._playingQueue.enqueue(orderInfo)
      this._renderQueueItem(orderInfo)
    }
  }

  _renderQueueItem (orderInfo) {
    const innerHtml = this._buildQueueItemHtml(orderInfo)
    $('#order-queue').append(innerHtml)
  }

  _buildQueueItemHtml (orderInfo) {
    const transformedFields = orderInfo.transformed_fields

    let orderInfoInnerHtml = ''
    for (const field in transformedFields) {
      orderInfoInnerHtml += '<label class="label-field">'
      orderInfoInnerHtml += transformedFields[field]
      orderInfoInnerHtml += '</label>'
    }

    let queueInnerHtml = ''
    queueInnerHtml += '<div id="'
    queueInnerHtml += orderInfo.unique_id
    queueInnerHtml += '" class="queue-item">'
    queueInnerHtml += '<div class="queued-order-cup-image">'
    queueInnerHtml += '<div class="thumbnail">'
    queueInnerHtml += '<img src='
    queueInnerHtml += orderInfo.captured_frame
    queueInnerHtml += ' width="100%" height="100%" />'
    queueInnerHtml += '</div>'
    queueInnerHtml += '</div>'
    queueInnerHtml += '<div id="audio-icon" class="audio-icon-outer-container" style="display:none">'
    queueInnerHtml += '<div class="audio-icon-inner-container">'
    queueInnerHtml += '<img src ="images/audio.gif" width="100%" height="100%" />'
    queueInnerHtml += '</div>'
    queueInnerHtml += '</div>'
    queueInnerHtml += '<div id="thumbsup-icon" class="thumbsup-icon-outer-container" style="display:none">'
    queueInnerHtml += '<div class="thumbsup-icon-inner-container">'
    queueInnerHtml += '<svg height="40%" viewBox="0 0 26 31" fill="none" xmlns="http://www.w3.org/2000/svg">'
    queueInnerHtml += '<path d="M16.2392 0.0828071C15.0287 -0.279692 14.0677 0.614208 13.7536 1.47846C13.574 1.97262 13.4098 2.431 13.2558 2.86089C12.6428 4.57192 12.1914 5.83196 11.5745 7.10102C9.62782 11.1057 7.14263 14.2401 2.49659 16.393C0.723216 17.2148 -0.414838 19.2106 0.142546 21.2331L1.04875 24.5211C1.56761 26.4038 3.05689 27.8541 4.9388 28.3094L15.2746 30.8098C18.8437 31.6732 22.4468 29.5186 23.4129 25.9431L25.8618 16.8804C26.5313 14.4028 24.6844 11.9606 22.1412 11.9606H18.4387C18.9636 10.1502 19.366 7.93176 19.3498 5.91457C19.3397 4.66164 19.1681 3.41617 18.7099 2.38026C18.241 1.32024 17.4517 0.445898 16.2392 0.0828071Z" fill="#4CAD76"/>'
    queueInnerHtml += '</svg>'
    queueInnerHtml += '</div>'
    queueInnerHtml += '</div>'
    queueInnerHtml += '<div class="queued-order-info">'
    queueInnerHtml += orderInfoInnerHtml
    queueInnerHtml += '</div>'
    queueInnerHtml += '<div id="announcing-text" class="announcing-text" style="display:none">'
    queueInnerHtml += '<label>Announcing</label>'
    queueInnerHtml += '</div>'
    queueInnerHtml += '</div>'

    return queueInnerHtml
  }

  _showPlayingOrderDetails () {
    if (this._removedQueueItem !== null) {
      $('#' + this._removedQueueItem.unique_id).remove()
    }
    const orderInfo = this._playingQueue.peek()
    if (orderInfo && orderInfo.value.audio_byte) {
      clearInterval(this._playAudioIntervalId)
      $('#audio-icon:last').show()
      $('#announcing-text').show()
      this._playAudio(orderInfo.value.audio_byte, () => { this._onEndedCallback(this) })
    }
  }

  _playAudio (audioByte, onEndedCallback) {
    const byteAudio = Uint8Array.from(atob(audioByte), c => c.charCodeAt(0))
    const buffer = new Uint8Array(byteAudio.length)
    buffer.set(new Uint8Array(byteAudio), 0)
    this._audioProcessor.playByteArray(buffer.buffer, onEndedCallback)
  }

  _onEndedCallback (self) {
    $('#audio-icon:last').hide()
    $('#announcing-text').hide()
    $('#thumbsup-icon:last').show()
    self._removedQueueItem = self._playingQueue.dequeue()
    self._processQueueItems()
  }
}
