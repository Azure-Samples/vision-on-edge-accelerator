import unittest
from unittest.mock import patch
from unittest import mock
import uuid
import os
from src.common.config_handler import ConfigHandler


class TestConfigHandler(unittest.TestCase):
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

    @mock.patch.dict(os.environ, {"BLOB_STORAGE_CONN_STRING": "test_conn_string"})
    @mock.patch.dict(os.environ, {"AZURE_BLOB_STORAGE_CONTAINER_NAME": "democontainer"})
    def test_get_storage_config(self):
        config_handler = ConfigHandler()
        str_config = config_handler.get_storage_config()
        assert str_config is not None

    @mock.patch.dict(os.environ, {"NUM_IMAGES_CAP_PER_HOUR": "60"})
    def test_get_sampler_config(self):
        config_handler = ConfigHandler()
        slr_config = config_handler.get_sampler_config()
        assert slr_config is not None

    @mock.patch.dict(
        os.environ, {"AZURE_COGNITIVE_SERVICE_FORMRECOG_KEY": "test_conn_string"}
    )
    @mock.patch.dict(
        os.environ, {"AZURE_COGNITIVE_SERVICE_FORMRECOG_ENDPOINT": "demo_endpoint"}
    )
    @mock.patch.dict(
        os.environ, {"AZURE_COGNITIVE_SERVICE_FORMRECOG_MODEL_ID": "demo_model"}
    )
    def test_get_az_ocr_config(self):
        config_handler = ConfigHandler()
        az_cogs_config = config_handler.get_az_cogs_formrecog_config()
        assert az_cogs_config is not None

    @mock.patch.dict(
        os.environ, {"AZURE_COGNITIVE_SERVICE_SPEECH_KEY": "test_conn_string"}
    )
    @mock.patch.dict(
        os.environ, {"AZURE_COGNITIVE_SERVICE_SPEECH_ENDPOINT": "demo_endpoint"}
    )
    @mock.patch.dict(os.environ, {"AZURE_COGNITIVE_SERVICE_SPEECH_TIMEOUT": "1.0"})
    def test_get_az_tts_config(self):
        config_handler = ConfigHandler()
        az_tts_config = config_handler.get_az_cogs_tts_config()
        assert az_tts_config is not None

    @mock.patch.dict(os.environ, {"DUPLICATE_ORDER_CACHE_MAX_LENGTH": "3"})
    @mock.patch.dict(os.environ, {"DUPLICATE_ORDER_CACHE_MAX_AGE_IN_SECONDS": "4"})
    def test_get_duplicate_order_cache_config(self):
        config_handler = ConfigHandler()
        duplicate_order_cache_config = config_handler.get_duplicate_order_cache_config()
        assert duplicate_order_cache_config is not None
