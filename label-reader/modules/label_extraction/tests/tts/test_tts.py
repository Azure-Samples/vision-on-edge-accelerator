import unittest
from unittest.mock import MagicMock, patch
from src.tts.tts import TTS


class TestTTS(unittest.TestCase):
    @patch("src.tts.tts.TTSPreprocessing")
    @patch("src.tts.tts.AzureTTS")
    def test_tts_check_if_azure_tts_and_pre_processing_called_once(
        self, mock_azure_tts, mock_pre_processing
    ):
        # Arrange
        tts_config = MagicMock()
        azure_tts_config = MagicMock()
        logger = MagicMock()
        tts_obj = TTS(tts_config, azure_tts_config, logger)
        template_vars = MagicMock()
        # Act
        tts_obj.run(template_vars)
        # Assert
        mock_azure_tts.assert_called_once()
        mock_pre_processing.assert_called_once()
        logger.error.assert_not_called()

    @patch("src.tts.tts.TTSPreprocessing")
    @patch("src.tts.tts.AzureTTS")
    def test_tts_not_sending_file_in_case_of_no_audio(
        self, mock_azure_tts, mock_pre_processing
    ):
        # Arrange
        tts_config = MagicMock()
        azure_tts_config = MagicMock()
        logger = MagicMock()
        mock_pre_processing().generate_ssml_payload.return_value = None
        tts_obj = TTS(tts_config, azure_tts_config, logger)
        template_vars = MagicMock()
        # Act
        tts_obj.run(template_vars)
        # Assert
        mock_azure_tts().call_tts.assert_not_called()
        mock_pre_processing().generate_ssml_payload.assert_called_once()
        logger.error.assert_called_once()
