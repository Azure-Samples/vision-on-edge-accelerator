export class AdminControlMessage {
  constructor (message) {
    this.command = message.command
    this.type = message.type
    this.status = message.status
  }
}
