import os
import unittest
import uuid
from unittest import mock
from unittest.mock import patch

from src.common.config_handler import ConfigHandler


class TestWebappApiConfigs(unittest.TestCase):
    def test_storage_config_load_success(self):
        @mock.patch.dict(os.environ, {"BLOB_STORAGE_CONN_STRING": "dummy"})
        @mock.patch.dict(os.environ, {"AZURE_BLOB_STORAGE_CONTAINER_NAME": "dummy"})
        def test_get_storage__config(self):
            config_handler = ConfigHandler()
            storage_config = config_handler.get_storage_config()
            assert storage_config is not None

    def test_webappapi_config_load_success(self):
        def test_get_webappapi__config(self):
            config_handler = ConfigHandler()
            api_config = config_handler.get_webapp_api_config()
            assert api_config is not None

    @patch(
        "src.common.config_handler.ConfigHandler._read_env_variable",
        side_effect=Exception("test"),
    )
    def test_get_config_throw_if_config_not_found(self, _):
        config_handler = ConfigHandler()
        self.assertRaises(
            Exception,
            config_handler.get_config,
            str(uuid.uuid1()),
        )

    def test_get_config_returns_config_if_found(self):
        config_handler = ConfigHandler()
        with patch(
            "src.common.config_handler.ConfigHandler._read_env_variable",
            return_value="test",
        ):
            self.assertEqual(config_handler.get_config("test"), "test")

    def test_get_config_raises_error_if_config_source_is_not_supported(self):
        config_handler = ConfigHandler(config_source="test")
        self.assertRaises(
            ValueError,
            config_handler.get_config,
            str(uuid.uuid1()),
        )

    def test__read_env_variable_throw_if_config_not_found(self):
        config_handler = ConfigHandler()
        self.assertRaises(
            ValueError, config_handler._read_env_variable, str(uuid.uuid1())
        )

    def test__read_env_variable_returns_config_if_found(self):
        config_handler = ConfigHandler()
        with patch(
            "src.common.config_handler.os.environ.get",
            return_value="test",
        ):
            self.assertEqual(config_handler._read_env_variable("test"), "test")
