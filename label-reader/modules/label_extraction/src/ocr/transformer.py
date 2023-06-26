"""This module is used to provide the ocr result transformation."""
from src.ocr.model import OrderLabelInfo
import re


class OcrResultTransformer:
    """
    Class for ocr result transformer
    """

    def __init__(
        self,
    ) -> None:
        """
        Initialize the class
        """
        self.cleanup_field_for_tts_regex = re.compile(r"[^a-zA-Z\d\s]")

    def transform_field_for_tts(self, field_info: OrderLabelInfo) -> str:
        """
        Transform field to remove special characters before sending to tts

        @param
            field_info (OrderLabelInfo): Azure Form Recognizer result with field information
        @return
            str: transformed field
        """

        return (
            self.cleanup_field_for_tts_regex.sub("", field_info.field_value)
            .strip()
            .upper()
        )
