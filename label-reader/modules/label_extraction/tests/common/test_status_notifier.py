import unittest
from unittest.mock import Mock
from src.common.status import ErrorCode
from src.edgeinferencing.result import TextDetectionResult
from src.frameprocessor.status_notifier import StatusNotifier
from src.validators.text_detection_validator import TextDetectionValidationResult


class TestStatusNotifier(unittest.TestCase):
    def test_notify_returns_low_bb_error(self):
        status_ws = Mock()
        status_notifier = StatusNotifier(status_ws)
        result = TextDetectionResult(
            validation_result=TextDetectionValidationResult(
                is_valid=False,
                error_code=ErrorCode.LOW_BB,
                bounding_box_detected=0,
                bounding_box_threshold_low=0,
                bounding_box_threshold_label=0,
            ),
            boxes=None,
            image=None,
        )
        self.assertTrue(status_notifier.notify(result, ""))
        status_ws.send.assert_called_once()
