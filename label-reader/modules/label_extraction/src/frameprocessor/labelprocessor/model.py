"""This module is used to provide the ocr request model."""
import numpy as np

from src.validators.ocr_validator import OcrValidationResult
from src.ocr.model import OrderLabelFieldInfo


class LabelProcessingRequest:
    """
    LabelProcessorRequest class.
    """

    def __init__(self, image: np.ndarray) -> None:
        """
        Initialize the LabelProcessorRequest class.

        @param
            image (np.ndarray): image
        """
        self.image = image


class LabelProcessingResponse:
    """
    LabelProcessorRequest class.
    """

    def __init__(
        self,
        extracted_result: dict[str, OrderLabelFieldInfo],
        validation_result: OcrValidationResult,
        transformed_result: dict[str, str],
        hash_identity: str,
        content_for_narration: dict[str, str],
        content_for_ui: dict[str, str],
    ) -> None:
        self.extracted_result = extracted_result
        self.transformed_result = transformed_result
        self.validation_result = validation_result
        self.hash_identity = hash_identity
        self.content_for_ui = content_for_ui
        self.content_for_narration = content_for_narration
