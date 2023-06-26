# Standard library imports...
from unittest.mock import patch, MagicMock
import unittest
from src.tts.az_cogs.azure_tts import AzureTTS
from src.tts.model import (
    TTSExceptionConnectionError,
    TTSExceptionHttpError,
    TTSExceptionUnknownError,
)
from src.tts.az_cogs.config import AzureTTSConfig
import logging
import requests


class TestAzureTtscaller(unittest.TestCase):
    @patch("requests.post")
    def test_success_path(self, mock_post):
        print("------ Running Unit Test - happy path scenario -------")
        # Configure the mock to return a response with an OK status code.
        l_audio_content = success_custom_response()
        mock_post.return_value = l_audio_content
        # manually set required configurations with dummy values
        l_tts_config = AzureTTSConfig("dummy", "dummy url", None)
        l_logger = logging.getLogger()
        tts_obj = AzureTTS(l_tts_config, l_logger)
        # Call the mock api
        responseobject = tts_obj.call_tts(MagicMock())
        self.assertEqual(str(responseobject.audio_content), l_audio_content.content)
        print("------ Success! Running Unit Test - for happy path -------")

    @patch("requests.post")
    def test_http_error_path(self, mock_post):
        # Configure the mock to return a response with an HTTP Error status.
        print("------ Running Unit Test - HTTP Error Scenario -------")
        l_audio_content = failure_custom_response()
        mock_post.return_value = l_audio_content
        # manually set required configurations with dummy values
        l_tts_config = AzureTTSConfig("dummy", "dummy url", None)
        l_logger = logging.getLogger()
        tts_obj = AzureTTS(l_tts_config, l_logger)
        # Call the mock api.
        with self.assertRaises(TTSExceptionHttpError):
            tts_obj.call_tts(MagicMock())
        print("------ Success! Running Unit Test - HTTP Error scenario -------")

    @patch("requests.post")
    def test_connection_error_path(self, mock_post):

        print("------ Running Unit Test - connection error -------")
        # Configure the mock to return a response with a connection error
        mock_post.side_effect = requests.exceptions.ConnectionError("connection error")
        # manually set required configurations with dummy values
        l_tts_config = AzureTTSConfig("dummy", "dummy url", None)
        l_logger = logging.getLogger()
        tts_obj = AzureTTS(l_tts_config, l_logger)
        # Call the mock api
        with self.assertRaises(TTSExceptionConnectionError):
            tts_obj.call_tts(MagicMock())
        print("------ Success! Running Unit Test - Connection Error scenario -------")

    @patch("requests.post")
    def test_unknown_error_path(self, mock_post):
        print("------ Running Unit Test - unknown error -------")
        # Configure the mock to return a response with a connection error
        mock_post.side_effect = Exception("unknown error")
        # manually set required configurations with dummy values
        l_tts_config = AzureTTSConfig("dummy", "dummy url", None)
        l_logger = logging.getLogger()
        tts_obj = AzureTTS(l_tts_config, l_logger)
        # Call the mock api
        with self.assertRaises(TTSExceptionUnknownError):
            tts_obj.call_tts(MagicMock())
        print("------ Success! Running Unit Test - unknown Error scenario -------")


class success_custom_response:
    def __init__(self):
        self.content = "some audio content"
        self.ok = True
        self.status_code = 200


class failure_custom_response:
    def __init__(self):
        self.content = ""
        self.ok = False
        self.status_code = 403


if __name__ == "__main__":
    unittest.main()
