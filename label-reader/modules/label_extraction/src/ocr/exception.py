"""This module is used to provide the exception for ocr."""


class OcrProcessException(Exception):
    """
    Class for ocr process exception
    """

    def __init__(self, *args: object) -> None:
        """
        Initializes the exception.

        @param
        args (object): args
        """
        super().__init__(*args)
