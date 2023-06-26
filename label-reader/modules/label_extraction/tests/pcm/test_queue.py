import multiprocessing
import time
import unittest
from src.pcm.queue import ProcessQueue


class TestProcessQueue(unittest.TestCase):
    def test_add_item_when_queue_is_empty(self):
        """Test to add item to queue."""
        queue = ProcessQueue()
        queue.add_item("test")
        time.sleep(0.1)
        self.assertEqual(queue.get_item(), "test")

    def test_add_item_replaces_existing_item_in_queue(self):
        """Test to add item to queue and replace existing item in queue."""
        queue = ProcessQueue()
        queue.add_item("test")
        time.sleep(0.1)
        queue.add_item("test2")
        time.sleep(0.1)
        self.assertEqual(queue.get_item(), "test2")
        self.assertTrue(queue.is_empty())

    def test_get_item_when_queue_is_not_empty(self):
        """Test to get item from queue."""
        queue = ProcessQueue()
        queue.add_item("test")
        time.sleep(0.1)
        self.assertEqual(queue.get_item(), "test")

    def test_get_item_when_queue_is_empty(self):
        """Test to get item from empty queue."""
        queue = ProcessQueue()
        time.sleep(0.1)
        self.assertIsNone(queue.get_item())

    def test_is_empty_when_queue_is_empty(self):
        """Test to check if queue is empty."""
        queue = ProcessQueue()
        self.assertTrue(queue.is_empty())

    def test_is_empty_when_queue_is_not_empty(self):
        """Test to check if queue is empty."""
        queue = ProcessQueue()
        queue.add_item("test")
        time.sleep(0.1)
        self.assertFalse(queue.is_empty())

    def test_clear_when_queue_is_empty(self):
        """Test to clear queue."""
        queue = ProcessQueue()
        time.sleep(0.1)
        queue.clear()
        self.assertTrue(queue.is_empty())

    def test_clear_when_queue_is_not_empty(self):
        """Test to clear queue."""
        queue = ProcessQueue()
        queue.add_item("test")
        time.sleep(0.1)
        queue.add_item("test2")
        time.sleep(0.1)
        queue.clear()
        self.assertTrue(queue.is_empty())

    def test_add_item_concurrent_insertion_from_multiple_process(self):
        """Test to add item to queue concurrently from multiple processes."""
        queue = ProcessQueue()
        processes = []
        for i in range(4):
            process = multiprocessing.Process(target=queue.add_item, args=(i,))
            processes.append(process)
        for process in processes:
            process.start()
        for process in processes:
            process.join()
        time.sleep(0.001)
        self.assertIsNotNone(queue.get_item())
        self.assertTrue(queue.is_empty())

    def test_concurrent_get_item_from_multiple_process(self):
        """Test to get item from queue concurrently from multiple processes."""
        queue = ProcessQueue()
        queue.add_item("test")
        processes = []
        for i in range(4):
            process = multiprocessing.Process(target=queue.get_item)
            processes.append(process)
        for process in processes:
            process.start()
        for process in processes:
            process.join()
        self.assertIsNone(queue.get_item())
        self.assertTrue(queue.is_empty())

    def test_add_item_timeout_if_lock_is_not_released(self):
        """Test to add item to queue with timeout if lock is not released."""
        queue = ProcessQueue()
        queue.locker.acquire()
        result = queue.add_item("test")
        self.assertFalse(result)
        queue.locker.release()
        self.assertTrue(queue.is_empty())

    def test_get_item_timeout_if_lock_is_not_released(self):
        """Test to get item to queue with timeout if lock is not released."""
        queue = ProcessQueue()
        queue.add_item("test")
        is_locked = queue.locker.acquire(block=True)
        self.assertTrue(is_locked)
        result = queue.get_item()
        self.assertIsNone(result)
        queue.locker.release()
        time.sleep(0.1)
        self.assertFalse(queue.is_empty())
