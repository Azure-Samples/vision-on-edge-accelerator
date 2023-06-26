"""This module is used to provide pre processing for tts."""
import os
from src.tts.model import TTSConfig
from pathlib import Path
from logging import Logger


class TTSPreprocessing:
    """
    Class for tts pre processing.
    """

    def __init__(self, config: TTSConfig, logger: Logger):
        """
        Initializes the tts pre processing.

        @param
            config (TTSConfig): tts config object
        """
        self.config = config
        self.logger = logger

    def generate_ssml_payload(
        self,
        template_vars: {},
    ) -> str:
        """
        Generates the ssml payload with pre-configured style, rate, language, etc.

        @param
            template_vars (dict): contains key value needed for the narration template
        @return
            ssml_payload (Optional(str)): ssml payload if all template_vars are present else None
        """
        ssml_payload = None
        template_file = os.path.join(
            os.path.dirname(__file__), "..", "templates", "narration-content.tpl"
        )
        tpl_content = Path(template_file).read_text()
        speech_config = {
            "language": self.config.speech_synthesis_language,
            "voice_name": self.config.speech_synthesis_voice_name,
            "style": self.config.speech_synthesis_style,
            "profile_rate": self.config.speech_synthesis_profile_rate,
            "profile_pitch": self.config.speech_synthesis_profile_pitch,
        }
        try:
            ssml_payload = tpl_content.format_map({**speech_config, **template_vars})
        except KeyError as err:
            self.logger.error(f"Missing keys. {err.args[0]}")
        return ssml_payload
