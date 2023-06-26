export class Feedback {
  constructor (message) {
    this.order_type = message.order_type
    this.order_number = message.order_number
    this.captured_frame = message.captured_frame.replace('data:image/jpeg;base64,', '')
    this.correlation_id = message.correlation_id
    this.device_id = message.device_id
    this.store_id = message.store_id
  }
}
