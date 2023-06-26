"""This module is used to provide process queue for communication between processes."""
import multiprocessing
from typing import Any


class ProcessQueue:
    """
    Process queue for communication between processes.
    """

    def __init__(self) -> None:
        """
        Initialize the process queue, with max length of 1.
        """
        self.maxlen = 1
        self.work_queue = multiprocessing.Queue(self.maxlen)
        self.locker = multiprocessing.Lock()
        self.locker_timeout = 0.5
        self.get_timeout = 0.5
        self.put_timeout = 0.5

    def add_item(self, item: Any) -> bool:
        """
        Add item to the queue and lock the queue durring adding.

        @param:
            item (Any): item object to be added to the queue
        @return:
            is_added (bool): True if the item is added, False otherwise
        """
        # multiprocessing.Lock can handle maximum processes matching the number of cores
        if self.locker.acquire(timeout=self.locker_timeout):
            self.clear()
            try:
                self.work_queue.put(item, timeout=self.put_timeout)
            except Exception:
                self.locker.release()
                return False
            self.locker.release()
            return True
        else:
            return False

    def get_item(self) -> Any:
        """
        Get item from the queue.

        @return:
            item (Any): item object from the queue
        """
        if not self.is_empty():
            if self.locker.acquire(timeout=self.locker_timeout):
                item = self.work_queue.get(timeout=self.get_timeout)
                self.locker.release()
                return item
        return None

    def is_empty(self) -> bool:
        """
        Check if the queue is empty.

        @return:
            is_empty (bool): True if the queue is empty, False otherwise
        """
        return self.work_queue.empty()

    def clear(self) -> None:
        """
        Clear the queue.
        """
        while not self.is_empty():
            try:
                self.work_queue.get(block=False)
            except Exception as ex:
                print(ex)
