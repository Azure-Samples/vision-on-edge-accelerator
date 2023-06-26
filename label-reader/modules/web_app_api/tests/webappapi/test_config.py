import unittest
from src.util.config import StorageConfig, WebappApiConfig


class TestWebappApiConfigs(unittest.TestCase):
    def test_storage_config_load_success(self):
        l_storage_config = StorageConfig("dummy conn string", "dummy container name")
        self.assertEqual(l_storage_config.blob_storage_conn_string, "dummy conn string")
        self.assertEqual(l_storage_config.container_name, "dummy container name")
        print("Config - Test-storage-load config")

    def test_webapp_api_config_load_success(self):
        l_api_config = WebappApiConfig()
        l_api_config.enable_compression()
        self.assertEqual(l_api_config.compression_is_enabled, True)
        print("Config - Test-webapp_api-load config")
