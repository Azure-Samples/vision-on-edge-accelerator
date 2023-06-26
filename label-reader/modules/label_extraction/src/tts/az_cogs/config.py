"""This module is used to provide all models for azure tts."""


class AzureTTSConfig:

    """Contains all the configurations specific to Azure Cognitive Services -
    Text to Speech Service.
    """

    def __init__(
        self,
        subscription_key: str,
        cogs_tts_endpoint: str,
        cogs_tts_timeout: float,
    ) -> None:
        """Initializes the configuration for the TTS calls

        Args:
            subscription_key (str): azure cognitive services - tts endpoint api key
            cogs_tts_endpoint (str): endpoint URL of the REST Service
            cogs_tts_timeout (float): timeout for the REST Service

        Deafaults:
            l_text_encoding (str): UTF-8
            l_audio_output_format (str): audio-16khz-64kbitrate-mono-mp3
        """
        self.l_subscription_key = subscription_key
        self.l_cogs_tts_endpoint = cogs_tts_endpoint
        self.l_timeout = cogs_tts_timeout
        self.l_text_encoding = "utf-8"
        self.l_audio_output_format = "audio-16khz-64kbitrate-mono-mp3"
