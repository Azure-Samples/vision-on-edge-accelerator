from typing import Union
from src.common.status import ErrorCode


class TextDetectionValidationResult:
    def __init__(
        self,
        is_valid: bool,
        error_code: Union[ErrorCode, None],
        bounding_box_detected: int,
        bounding_box_threshold_low: int,
        bounding_box_threshold_label: int,
    ):
        self.is_valid = is_valid
        self.error_code = error_code
        self.bounding_box_detected = bounding_box_detected
        self.bounding_box_threshold_low = bounding_box_threshold_low
        self.bounding_box_threshold_label = bounding_box_threshold_label

    def __str__(self):
        return f"TextDetectionValidationResult(is_valid={self.is_valid}, error_code={self.error_code}, bounding_box_detected={self.bounding_box_detected}, bounding_box_threshold_low={self.bounding_box_threshold_low}), bounding_box_threshold_label={self.bounding_box_threshold_label}"  # noqa E501


class TextDetectionValidator:
    def __init__(
        self, bounding_box_threshold_low: int, bounding_box_threshold_label: int
    ):
        self.bounding_box_threshold_low = bounding_box_threshold_low
        self.bounding_box_threshold_label = bounding_box_threshold_label

    def validate(self, bounding_box_detected: int) -> TextDetectionValidationResult:
        if bounding_box_detected < self.bounding_box_threshold_low:
            return TextDetectionValidationResult(
                is_valid=False,
                error_code=ErrorCode.NO_CUP,
                bounding_box_detected=bounding_box_detected,
                bounding_box_threshold_low=self.bounding_box_threshold_low,
                bounding_box_threshold_label=self.bounding_box_threshold_label,
            )
        elif (
            self.bounding_box_threshold_low
            <= bounding_box_detected
            < self.bounding_box_threshold_label
        ):
            return TextDetectionValidationResult(
                is_valid=False,
                error_code=ErrorCode.LOW_BB,
                bounding_box_detected=bounding_box_detected,
                bounding_box_threshold_low=self.bounding_box_threshold_low,
                bounding_box_threshold_label=self.bounding_box_threshold_label,
            )
        else:
            return TextDetectionValidationResult(
                is_valid=True,
                error_code=None,
                bounding_box_detected=bounding_box_detected,
                bounding_box_threshold_low=self.bounding_box_threshold_low,
                bounding_box_threshold_label=self.bounding_box_threshold_label,
            )
