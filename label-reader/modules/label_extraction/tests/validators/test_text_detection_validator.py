import unittest
from src.common.status import ErrorCode
from src.validators.text_detection_validator import TextDetectionValidator


class TestTextDetectionValidator(unittest.TestCase):
    @classmethod
    def setUp(cls):
        cls.validator = TextDetectionValidator(
            bounding_box_threshold_low=1,
            bounding_box_threshold_label=3,
        )

    def test_validate_returns_no_cup_when_bounding_box_detected_is_less_than_threshold_low(
        self,
    ):

        result = self.validator.validate(bounding_box_detected=0)
        self.assertEqual(result.is_valid, False)
        self.assertEqual(result.error_code, ErrorCode.NO_CUP)

    def test_validate_returns_valid_result_when_bounding_box_detected_is_same_as_threshold_low(
        self,
    ):
        result = self.validator.validate(bounding_box_detected=1)
        self.assertEqual(result.is_valid, False)
        self.assertEqual(result.error_code, ErrorCode.LOW_BB)

    def test_validate_returns_low_bb_when_bounding_box_detected_is_between_threshold_low_and_threshold_label(
        self,
    ):
        result = self.validator.validate(bounding_box_detected=2)
        self.assertEqual(result.is_valid, False)
        self.assertEqual(result.error_code, ErrorCode.LOW_BB)

    def test_validate_returns_low_bb_when_bounding_box_detected_is_same_as_threshold_label(
        self,
    ):
        result = self.validator.validate(bounding_box_detected=3)
        self.assertEqual(result.is_valid, True)
        self.assertEqual(result.error_code, None)

    def test_validate_returns_valid_result_when_bounding_box_detected_is_greater_than_threshold_label(
        self,
    ):
        result = self.validator.validate(bounding_box_detected=4)
        self.assertEqual(result.is_valid, True)
        self.assertEqual(result.error_code, None)
