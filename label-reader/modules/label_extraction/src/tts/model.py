"""This module is used to provide all models for tts."""


class TTSResponse:
    """
    Class for tts response model.
    """

    def __init__(self, audio_content: bytes) -> None:
        """
        Initializes the tts response.

        @param
            audio_content (bytes): audio content
        """
        self.audio_content = audio_content


class TTSConfig:
    """
    Class for tts config model.
    """

    def __init__(
        self,
        speech_synthesis_voice_name: str,
        speech_synthesis_language: str,
        speech_synthesis_style: str,
        speech_synthesis_profile_rate: str,
        speech_synthesis_profile_pitch: str,
    ) -> None:
        """
        Initializes the tts config.

        @param
            speech_synthesis_voice_name (str): voice name
            speech_synthesis_language (str): voice language
            speech_synthesis_style (str): voice style
            speech_synthesis_profile_rate (str): voice rate
            speech_synthesis_profile_pitch (str): voice pitch
        """
        self.speech_synthesis_voice_name = speech_synthesis_voice_name
        self.speech_synthesis_language = speech_synthesis_language
        self.speech_synthesis_style = speech_synthesis_style
        self.speech_synthesis_profile_rate = speech_synthesis_profile_rate
        self.speech_synthesis_profile_pitch = speech_synthesis_profile_pitch


class TTSExceptionHttpError(Exception):
    """
    Exception for http error.
    """

    def __init__(self, *args: object) -> None:
        """
        Initializes the exception.

        @param
            args (object): args
        """
        super().__init__(*args)


class TTSExceptionConnectionError(Exception):
    """
    Exception for connection error.
    """

    def __init__(self, *args: object) -> None:
        """
        Initializes the exception.

        @param
            args (object): args
        """
        super().__init__(*args)


class TTSExceptionUnknownError(Exception):
    """
    Exception for unknown error.
    """

    def __init__(self, *args: object) -> None:
        """
        Initializes the exception.

        @param
            args (object): args
        """
        super().__init__(*args)
