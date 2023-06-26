import unittest
from src.common.storage_helper import StorageServiceHelper
from src.util.config import StorageConfig
import json
from src.util import log_helper


class TestStorageHelper(unittest.TestCase):
    def test_set_config_exception(self):

        # helper_obj.l_config = StorageConfig("dummy conn string", "dummy container name")
        storage_config = StorageConfig("dummy conn string", "dummy container name")
        s_helper = StorageServiceHelper(log_helper.get_logger(), storage_config)
        StorageServiceHelper.trace_logger = log_helper.get_logger()
        result = s_helper.verify_upload_frame("dummy")
        self.assertIsNone(result)
        print("StorageHelper - Test - set config raise exception")

    def test_verify_invalid_input_no_error(self):
        storage_config = StorageConfig("dummy conn string", "dummy container name")
        helper_obj = StorageServiceHelper(log_helper.get_logger(), storage_config)
        StorageServiceHelper.trace_logger = log_helper.get_logger()

        res_obj = helper_obj.verify_upload_frame(json.dumps(self.feedback_msg_invalid))
        self.assertIs(res_obj, None)
        print("StorageHelper - Test - invalid input no error")

    def test_verify_throw_decode_error(self):
        storage_config = StorageConfig("dummy conn string", "dummy container name")
        helper_obj = StorageServiceHelper(log_helper.get_logger(), storage_config)
        StorageServiceHelper.trace_logger = log_helper.get_logger()

        res_obj = helper_obj.verify_upload_frame(
            json.dumps(self.feedback_msg_complete_but_invalid)
        )
        self.assertIs(res_obj, None)
        print("StorageHelper - Test - invalid input decode error")

    feedback_msg_complete_but_invalid = {
        "order_type": "店用",
        "order_number": "35974",
        "captured_frame": "dummy frame data",
        "correlation_id": "99999sdsscxxrxzrabcd12312311234",
        "device_id": "dev0101",
        "store_id": "store0101",
    }

    feedback_msg_invalid = {
        "order_type": "店用",
        "order_number": "35974",
        "captured_frame": "dummy frame data",
        "correlation_id": "",
        "device_id": "dev0101",
        "store_id": "store0101",
    }

    feedback_msg_error = "this should raise an error"

    # @patch('azure.storage.blob.BlobServiceClient.from_connection_string')
    # @patch('azure.storage.blob.ContainerClient.create_container')
    # @patch('azure.storage.blob.BlobClient.upload_blob')
    # def test_upload_frame(self, mocka, mockb, mockc):
    #     helper_obj = StorageServiceHelper()
    #     helper_obj.l_config = StorageConfig.getInstance('dummy conn string', 'dummy container name')
    #     mocka = MagicMock()
    #     mockb = MagicMock(mocka)
    #     mockc.return_value = 'dummy_url'
    #     resp = helper_obj._upload_frame(MagicMock(),MagicMock(), MagicMock(), MagicMock())
    #     print('BLOB UPLOAD RETURN VALUE ',resp)
    #     self.assertEquals(resp, 'dummy_url_abc')
