"""This module is used to provide Azure Form Recognizer output validation."""
from logging import Logger
from typing import Union
from src.ocr.model import OrderLabelFieldInfo

from src.common.status import ErrorCode


class OcrValidationResult:
    """
    This class is used to provide model for Azure Form Recognizer output validation
    """

    def __init__(
        self,
        is_valid: bool,
        error_code: Union[ErrorCode, None],
    ) -> None:
        """
        Initialize the class

        @param
            is_valid (bool): is valid
            error_code (Union[ErrorCode, None]): error code, None in case of valid
        """
        self.is_valid = is_valid
        self.error_code = error_code

    def __str__(self):
        """
        String representation of the class
        """
        return f"OcrValidationResult(is_valid={self.is_valid}, error_code={self.error_code}"  # noqa E501


class OcrResultValidator:
    """
    This class is used to validate Azure Form Recognizer output
    """

    def __init__(self, confidence_threshold: float, logger: Logger) -> None:
        """
        Initialize the class

        @param
            confidence_threshold (float): threshold for confidence
            logger (Logger): logger
        """
        self._logger = logger
        self.confidence_threshold = confidence_threshold

    def validate_field_is_empty(
        self, field_info: OrderLabelFieldInfo
    ) -> OcrValidationResult:
        """
        Validate if fields are not empty

        @param
            field_info (OrderLabelFieldInfo): Azure Form Recognizer result with field information
        @return
            OcrValidationResult: validation result
        """
        if field_info.field_value is None:
            return OcrValidationResult(False, ErrorCode.FIELD_MISSING)
        else:
            return OcrValidationResult(True, None)

    def validate_field_confidence(
        self, field_info: OrderLabelFieldInfo
    ) -> OcrValidationResult:
        """
        Validate if field confidence is greater than defined threshold

        @param
            field_info (OrderLabelFieldInfo): Azure Form Recognizer result with field information
        @return
            OcrValidationResult: validation result
        """
        if field_info.field_confidence < self.confidence_threshold:
            return OcrValidationResult(False, ErrorCode.LOW_FIELD_CONFIDENCE)
        else:
            return OcrValidationResult(True, None)
