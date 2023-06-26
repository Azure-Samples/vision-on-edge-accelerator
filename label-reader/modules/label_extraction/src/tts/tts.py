"""This module is used to provide tts pre, post and actual processing."""
from logging import Logger
from src.tts.az_cogs.config import AzureTTSConfig
from src.tts.az_cogs.azure_tts import AzureTTS
from src.tts.model import TTSConfig, TTSResponse
from src.tts.pre_processing import TTSPreprocessing


class TTS:
    """Class for tts pre, post and actual processing."""

    def __init__(
        self, tts_config: TTSConfig, azure_tts_config: AzureTTSConfig, logger: Logger
    ):
        """
        Initialize TTS class.

        @param
            tts_config (TTSConfig): TTS config object.
            azure_tts_config (AzureTTSConfig): Azure TTS config object.
            logger (Logger): Logger object.
        """
        self.tts_config = tts_config
        self.logger = logger
        self.azure_tts = AzureTTS(azure_tts_config, logger)
        self.pre_processing = TTSPreprocessing(tts_config, logger)

    def run(self, template_vars: {}) -> TTSResponse:
        """
        Run the tts pre, post and actual processing.

        @param
            template_vars (dict): contains key value needed for the narration template
        @return
            TTSResponse: TTS response object.
        """
        self.logger.debug("TTS process starting...")
        ssml_payload = self.pre_processing.generate_ssml_payload(template_vars)
        tts_response = None
        if ssml_payload is not None:
            tts_response = self.azure_tts.call_tts(ssml_payload)
        else:
            self.logger.error("Narration content wasn't generated. No audio file sent.")
        self.logger.debug("TTS process completed")
        return tts_response
