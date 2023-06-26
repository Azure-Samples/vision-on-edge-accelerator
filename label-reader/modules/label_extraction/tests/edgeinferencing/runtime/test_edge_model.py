import unittest
from unittest.mock import MagicMock, patch
import numpy as np
from src.common.status import ErrorCode
from src.edgeinferencing.edge_model import TextDetectionRequest

from src.edgeinferencing.config import (
    DBPostProcessConfig,
    EdgeModelConfig,
    TextDetectionValidationConfig,
)
from src.validators.text_detection_validator import TextDetectionValidationResult


class TestTextDetection(unittest.TestCase):
    @patch(
        "src.edgeinferencing.edge_model.Engine.inference_single",
        return_value=MagicMock(),
        autospec=True,
    )
    @patch(
        "src.edgeinferencing.edge_model.DBPostProcess.__call__",
        side_effect=lambda _, __: [{"points": [1]}],
    )
    @patch("src.edgeinferencing.edge_model.create_operators", return_value=MagicMock())
    @patch(
        "src.edgeinferencing.edge_model.transform",
        return_value=(MagicMock(), MagicMock()),
    )
    @patch("src.edgeinferencing.edge_model.np.reshape", return_value=MagicMock())
    @patch("src.edgeinferencing.edge_model.cv2.resize", return_value=MagicMock())
    def test_run_returns_correct_bounding_boxes(self, *args):
        from src.edgeinferencing.edge_model import TextDetection

        logger = MagicMock()
        model_config = EdgeModelConfig("", [""])
        text_detection_config = DBPostProcessConfig(0.1, 0.1, 1, 1, True, "fast")
        validation_config = TextDetectionValidationConfig(0, 0, False, 1)
        text_detection = TextDetection(
            text_detection_config, model_config, validation_config, logger
        )
        image = np.zeros((100, 100, 3))
        text_detection_result = text_detection.run(TextDetectionRequest(image=image))
        self.assertEqual(len(text_detection_result.boxes), 1)
        self.assertEqual(
            text_detection_result.validation_result.bounding_box_detected, 1
        )

    def test__skip_frame_check_if_frame_is_skipped(self):
        from src.edgeinferencing.edge_model import TextDetection

        logger = MagicMock()
        model_config = EdgeModelConfig("", [""])
        text_detection_config = DBPostProcessConfig(0.1, 0.1, 1, 1, True, "fast")
        # Skip 2 frames after the first detected valid frame
        validation_config = TextDetectionValidationConfig(0, 0, True, 2)
        text_detection = TextDetection(
            text_detection_config, model_config, validation_config, logger
        )
        validation_result = TextDetectionValidationResult(
            is_valid=False,
            error_code=ErrorCode.NO_CUP,
            bounding_box_detected=0,
            bounding_box_threshold_low=0,
            bounding_box_threshold_label=0,
        )
        validation_result = text_detection._skip_frame(validation_result)
        # Invalid frame should be skipped
        self.assertTrue(text_detection.skip_frame)
        self.assertEqual(validation_result.error_code, ErrorCode.NO_CUP)
        self.assertFalse(validation_result.is_valid)
        validation_result.is_valid = True
        validation_result.error_code = None
        validation_result = text_detection._skip_frame(validation_result)
        # Valid 1st frame should be skipped
        self.assertTrue(text_detection.skip_frame)
        self.assertEqual(validation_result.error_code, ErrorCode.SKIP_FRAME)
        self.assertFalse(validation_result.is_valid)
        validation_result.is_valid = True
        validation_result.error_code = None
        validation_result = text_detection._skip_frame(validation_result)
        # Valid 2nd frame should be skipped
        self.assertFalse(text_detection.skip_frame)
        self.assertEqual(validation_result.error_code, ErrorCode.SKIP_FRAME)
        self.assertFalse(validation_result.is_valid)
        validation_result.is_valid = True
        validation_result.error_code = None
        validation_result = text_detection._skip_frame(validation_result)
        # Valid 3rd frame should not be skipped
        self.assertFalse(text_detection.skip_frame)
        self.assertEqual(validation_result.error_code, None)
        self.assertTrue(validation_result.is_valid)
        validation_result.is_valid = False
        validation_result.error_code = ErrorCode.NO_CUP
        validation_result = text_detection._skip_frame(validation_result)
        # Invalid frame should reset counter
        self.assertTrue(text_detection.skip_frame)
        self.assertEquals(text_detection.skip_frame_counter, 2)

    def test__skip_frame_check_if_frame_is_skipped_with_invalid_result(self):
        from src.edgeinferencing.edge_model import TextDetection

        logger = MagicMock()
        model_config = EdgeModelConfig("", [""])
        text_detection_config = DBPostProcessConfig(0.1, 0.1, 1, 1, True, "fast")
        # Skip 2 frames after the first detected valid frame
        validation_config = TextDetectionValidationConfig(0, 0, True, 1)
        text_detection = TextDetection(
            text_detection_config, model_config, validation_config, logger
        )
        validation_result = TextDetectionValidationResult(
            is_valid=False,
            error_code=ErrorCode.NO_CUP,
            bounding_box_detected=0,
            bounding_box_threshold_low=0,
            bounding_box_threshold_label=0,
        )
        validation_result = text_detection._skip_frame(validation_result)
        # Invalid frame should be skipped
        self.assertTrue(text_detection.skip_frame)
        self.assertEqual(validation_result.error_code, ErrorCode.NO_CUP)
        self.assertFalse(validation_result.is_valid)
        validation_result.is_valid = True
        validation_result.error_code = None
        validation_result = text_detection._skip_frame(validation_result)
        # Valid 1st frame should be skipped
        self.assertFalse(text_detection.skip_frame)
        self.assertEqual(validation_result.error_code, ErrorCode.SKIP_FRAME)
        self.assertFalse(validation_result.is_valid)
        validation_result.is_valid = False
        validation_result.error_code = ErrorCode.LOW_BB
        validation_result = text_detection._skip_frame(validation_result)
        # Invalid 2nd frame should be skipped
        self.assertTrue(text_detection.skip_frame)
        self.assertEqual(validation_result.error_code, ErrorCode.LOW_BB)
        self.assertFalse(validation_result.is_valid)
