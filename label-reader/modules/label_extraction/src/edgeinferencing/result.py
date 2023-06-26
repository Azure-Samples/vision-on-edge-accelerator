"""This module is used to provide the text detection result object."""
from typing import List

import numpy as np
from src.validators.text_detection_validator import TextDetectionValidationResult


class TextDetectionResult:
    """
    TextDetectionResult class.
    """

    def __init__(
        self,
        validation_result: TextDetectionValidationResult,
        boxes: List,
        image: np.ndarray,
    ) -> None:
        """
        Initialize the TextDetectionResult class.

        @param
            validation_result (TextDetectionValidationResult): validation result
            boxes (List): bounding boxes
            image (np.ndarray): image
        """
        self.validation_result = validation_result
        self.boxes = boxes
        self.image = image
