import unittest
from unittest.mock import MagicMock, patch

# from src.common.sampler import BasicSampler
from src.common import log_helper
from src.frameprocessor.config import SamplerConfig, StorageConfig
from src.storage.storage_helper import StorageServiceHelper
from src.storage.storage_request import StorageUploadRequest
from src.common.sampler import BasicSampler


class TestStorageHelper(unittest.TestCase):
    def test_null_params_check(self):

        l_logger = log_helper.get_logger()
        s_config = StorageConfig("dummy string", "dummy container")
        samplerConfig = SamplerConfig(60)
        sampler = BasicSampler(l_logger, samplerConfig)
        s_helper = StorageServiceHelper(l_logger, s_config, sampler)
        req_obj = StorageUploadRequest(None, "None", None, None)
        result = s_helper.verify_upload_frame(req_obj)
        self.assertIsNone(result)

    def test_encode_error_check(self):

        l_logger = log_helper.get_logger()
        s_config = StorageConfig("dummy string", "dummy container")
        samplerConfig = SamplerConfig(60)
        sampler = BasicSampler(l_logger, samplerConfig)
        s_helper = StorageServiceHelper(l_logger, s_config, sampler)
        req_obj = StorageUploadRequest("dummy", "", "", "dummy")
        result = s_helper.verify_upload_frame(req_obj)
        self.assertIsNone(result)

    # def test_encode_error_check_threshold(self):

    #     l_logger = log_helper.get_logger()
    #     s_config = StorageConfig("dummy string", "dummy container")
    #     samplerConfig = SamplerConfig(10, 3600, 300)
    #     sampler = BasicSampler(l_logger, samplerConfig)
    #     s_helper = StorageServiceHelper(l_logger, s_config, sampler)
    #     req_obj = StorageUploadRequest("dummy", "dummy", "dummy", "dummy")
    #     result = None
    #     for i in range(0, 1100):
    #         result = s_helper.verify_upload_frame(req_obj)
    #     self.assertIsNone(result)

    def test_client_conn_error(self):
        l_logger = log_helper.get_logger()
        s_config = StorageConfig("dummy string", "dummy container")
        samplerConfig = SamplerConfig(60)
        sampler = BasicSampler(l_logger, samplerConfig)

        s_helper = StorageServiceHelper(l_logger, s_config, sampler)
        self.assertIsNone(s_helper.blob_service_client)
        # req_obj = StorageUploadRequest("dummy", "dummy", "dummy", "dummy")
        # result = s_helper._upload_frame(req_obj, "dummy")
        # self.assertIsNone(result)

    @patch("azure.storage.blob.BlobClient.from_connection_string")
    @patch("azure.storage.blob.BlobClient.upload_blob")
    def test_client_conn_success(self, mocka, mockb):
        l_logger = log_helper.get_logger()
        mocka.return_value = MagicMock()
        mockb.return_value = MagicMock()
        s_config = StorageConfig("dummy string", "dummy container")
        samplerConfig = SamplerConfig(60)
        sampler = BasicSampler(l_logger, samplerConfig)
        s_helper = StorageServiceHelper(l_logger, s_config, sampler)
        req_obj = StorageUploadRequest("dummy", "dummy", "dummy", "dummy")
        result = s_helper._upload_frame(req_obj, "dummy")
        self.assertIsNotNone(result)
