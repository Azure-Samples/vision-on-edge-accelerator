export class Node {
  constructor (elem) {
    this.value = elem
    this.next = null
  }
}

export class Queue {
  constructor () {
    this.head = null
    this.tail = null
    this.size = 0
  }

  isEmpty () {
    return this.size === 0
  }

  enqueue (elem) {
    const newNode = new Node(elem)
    if (!this.head) {
      this.head = newNode
      this.tail = newNode
    } else {
      this.tail.next = newNode
      this.tail = newNode
    }
    ++this.size
  }

  dequeue () {
    if (this.isEmpty()) {
      return null
    }

    const removedItem = this.head
    if (this.head === this.tail) {
      this.tail = null
    }
    --this.size
    this.head = this.head.next
    return removedItem.value
  }

  peek () {
    return this.head
  }

  length () {
    return this.size
  }
}
