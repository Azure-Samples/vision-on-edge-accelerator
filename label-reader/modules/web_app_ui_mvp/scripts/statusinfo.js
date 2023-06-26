export class StatusInfo {
  constructor (message) {
    this.is_cup_detected = message.is_cup_detected
    this.is_error = message.is_error
    this.error_code = message.error_code
    this.error_sub_type = message.error_sub_type
    this.correlation_id = message.correlation_id
    this.timestamp = message.timestamp
  }
}
