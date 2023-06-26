import unittest

from src.storage.storage_request import StorageUploadRequest


class TestStorageUploadRequest(unittest.TestCase):
    def test_request_object(self):
        upload_req = StorageUploadRequest("dummy", "corrid", "device_id", "store_id")
        self.assertIsNotNone(upload_req)
