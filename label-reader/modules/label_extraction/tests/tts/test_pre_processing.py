import unittest
from src.tts.pre_processing import TTSPreprocessing
from src.tts.model import TTSConfig
from unittest.mock import MagicMock


class TestPreProcessing(unittest.TestCase):
    logger = MagicMock()

    @classmethod
    def setUp(cls):
        cls.config = TTSConfig(
            speech_synthesis_voice_name="speech_synthesis_voice_name",
            speech_synthesis_language="speech_synthesis_language",
            speech_synthesis_style="speech_synthesis_style",
            speech_synthesis_profile_rate="speech_synthesis_profile_rate",
            speech_synthesis_profile_pitch="speech_synthesis_profile_pitch",
        )

        cls.pre_processing = TTSPreprocessing(cls.config, cls.logger)

    def test_generate_ssml_payload_for_given_customer_and_item_name(self):
        template_vars = {
            "item_name": "latte",
            "customer_name": "Jess",
        }

        expected_ssml_payload = f"""
        <speak xmlns="http://www.w3.org/2001/10/synthesis" xmlns:mstts="http://www.w3.org/2001/mstts" xmlns:emo="http://www.w3.org/2009/10/emotionml" version="1.0" xml:lang="{self.config.speech_synthesis_language}">
            <voice name="{self.config.speech_synthesis_voice_name}">
                <mstts:express-as style="{self.config.speech_synthesis_style}" >
                    <prosody rate="{self.config.speech_synthesis_profile_rate}" pitch="{self.config.speech_synthesis_profile_pitch}">
                        Hello Jess
                        your latte is ready
                    </prosody>
                </mstts:express-as>
            </voice>
        </speak>"""  # noqa: E501
        actual_ssml_payload = self.pre_processing.generate_ssml_payload(template_vars)
        self.assertEquals(actual_ssml_payload.split(), expected_ssml_payload.split())

    def test_generate_none_if_template_vars_has_missing_keys(self):
        template_vars = {
            "item_name": "latte",
        }

        actual_ssml_payload = self.pre_processing.generate_ssml_payload(template_vars)
        self.assertIsNone(actual_ssml_payload)
        self.logger.error.assert_called_once()
