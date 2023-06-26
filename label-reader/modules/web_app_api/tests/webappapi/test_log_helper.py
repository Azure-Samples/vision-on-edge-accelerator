"""Test src/util/test_log_helper."""
import unittest
from unittest.mock import patch
from unittest import mock
import os
import src.util.log_helper as log_helper


class TestLogHelper(unittest.TestCase):
    @patch("src.util.log_helper.app_insights_key", "")
    def test_get_logger_disabled(self):
        logger = log_helper.get_logger()
        assert logger is not None

    @patch("src.util.log_helper.app_insights_key", "test")
    @mock.patch.dict(os.environ, {"APPINSIGHTS_CONNECTION_STRING": "test"}, clear=True)
    def test_get_logger(self):
        with self.assertRaises(Exception):
            logger = log_helper.get_logger()
            assert logger is not None

    @patch("src.util.log_helper.app_insights_key", "")
    @mock.patch.dict(os.environ, {"APPINSIGHTS_CONNECTION_STRING": ""}, clear=True)
    def test_get_logger_empty_app_key(self):
        logger = log_helper.get_logger()
        assert logger is not None


if __name__ == "__main__":
    unittest.main()
