export class OrderInfo {
  constructor (message) {
    this.unique_id = Math.floor((Math.random()) * 0x10000).toString(16)
    this.transformed_fields = message.transformed_fields
    this.captured_frame = message.captured_frame
    this.audio_byte = message.audio_byte
    this.correlation_id = message.correlation_id
    this.device_id = message.device_id
    this.store_id = message.store_id
    this.timestamp = new Date().getTime()
  }
}
