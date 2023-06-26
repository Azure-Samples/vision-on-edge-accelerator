"""This module is used to provide the status details."""
from enum import Enum
import time


class ErrorCode(str, Enum):
    """
    Error codes enum.
    """

    LOW_BB = "LOW_BB"
    LOW_FIELD_CONFIDENCE = "LOW_FIELD_CONFIDENCE"
    FIELD_MISSING = "FIELD_MISSING"
    CUSTOMER_NAME_MISSING = "CUSTOMER_NAME_MISSING"
    ITEM_NAME_MISSING = "ITEM_NAME_MISSING"
    ORDER_TYPE_MISSING = "ORDER_TYPE_MISSING"
    NO_CUP = "NO_CUP"
    SKIP_FRAME = "SKIP_FRAME"

    EDGE_MODEL_ERROR = "EDGE_MODEL_ERROR"
    OCR_ERROR = "OCR_ERROR"
    LABEL_PROCESSING_ERROR = "LABEL_PROCESSING_ERROR"
    TTS_ERROR = "TTS_ERROR"


class StatusCode(str, Enum):
    """
    Status codes enum.
    """

    SYSTEM = "SYSTEM"
    LABEL_EXTRACTION = "LABEL_EXTRACTION"


class Status:
    """
    Status class.
    """

    def __init__(
        self,
        error_sub_type: ErrorCode,
        error_code: StatusCode,
        correlation_id: str,
        is_error: bool,
        is_cup_detected: bool = True,
    ):
        """
        Initialize Status.

        @param:
            error_sub_type (ErrorCode): error sub type
            error_code (StatusCode): error code
            correlation_id (str): correlation id
            is_error (bool): is error
            is_cup_detected (bool): is cup detected
        """
        self.error_sub_type = error_sub_type
        self.error_code = error_code
        self.correlation_id = correlation_id
        self.is_error = is_error
        self.is_cup_detected = is_cup_detected
        self.timestamp = time.time() * 1000
