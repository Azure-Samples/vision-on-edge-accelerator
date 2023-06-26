"""This module is used to provide a configuration class for ocr result validation."""


class OCRValidationConfig:
    """
    OCR result validation config class
    """

    def __init__(
        self,
        confidence_threshold: float,
    ) -> None:
        """
        Initialize the class

        @param
            confidence_threshold (float): confidence threshold
        """
        self.confidence_threshold = confidence_threshold
