"""This module is used to provide the edge model for text detection."""
from logging import Logger
from typing import List
import numpy as np
import cv2
from src.common.status import ErrorCode
from src.edgeinferencing.request import TextDetectionRequest
from src.edgeinferencing.result import TextDetectionResult

from src.edgeinferencing.common.postprocess_db import DBPostProcess
from src.edgeinferencing.common.preprocess_operator import create_operators, transform
from src.edgeinferencing.runtime.onnxruntime.engine import Engine
from src.edgeinferencing.config import (
    EdgeInferencingPreProcessConfig,
    EdgeModelConfig,
    DBPostProcessConfig,
    TextDetectionValidationConfig,
)
from src.validators.text_detection_validator import (
    TextDetectionValidationResult,
    TextDetectionValidator,
)


class TextDetection:
    """
    Class TextDetection.
    """

    def __init__(
        self,
        text_detection_config: DBPostProcessConfig,
        model_config: EdgeModelConfig,
        validation_config: TextDetectionValidationConfig,
        logger: Logger,
    ) -> None:
        """
        Initialize the TextDetection class.

        @param
            text_detection_config (DBPostProcessConfig): post-processing configuration for text detection
            model_config (EdgeModelConfig): configuration for edge model
            validation_config (TextDetectionValidationConfig): configuration for text detection validation
            logger (Logger): logger
        """
        self.pre_processors = create_operators(EdgeInferencingPreProcessConfig())
        self.post_process_op = DBPostProcess(
            thresh=text_detection_config.thresh,
            box_thresh=text_detection_config.box_thresh,
            max_candidates=text_detection_config.max_candidates,
            score_mode=text_detection_config.score_mode,
            unclip_ratio=text_detection_config.unclip_ratio,
            use_dilation=text_detection_config.use_dilation,
        )
        self.engine = Engine(model_config, logger)
        self.model_config = model_config
        self.logger = logger
        self.validation_config = validation_config

        self.validator = TextDetectionValidator(
            validation_config.bounding_box_threshold_low,
            validation_config.bounding_box_threshold_label,
        )

        self.skip_frame = False
        self.skip_frame_counter = validation_config.skip_frame_count

    def initialize(self):
        """
        Initialize the text detection edge engine as per platform
        """
        self.logger.info("Initializing Engine")
        self.engine.initialize()
        self.logger.info("Finished Initializing Engine")

    def _pre_process(self, image: np.ndarray) -> np.ndarray:
        """
        Pre process image.

        @param
            image (np.ndarray): image to be pre-processed
        @return
            image (np.ndarray): pre-processed image
        """
        return cv2.resize(image, self.model_config.image_size)

    def _post_process(self, bb_boxes: int) -> TextDetectionValidationResult:
        """
        Post process result.

        @param
            bb_boxes (int): number of bounding boxes detected
        @return
            validation_result (TextDetectionValidationResult): validation result
        """
        validation_result = self.validator.validate(bb_boxes)
        validation_result = self._skip_frame(validation_result)
        return validation_result

    def _skip_frame(
        self, validation_result: TextDetectionValidationResult
    ) -> TextDetectionValidationResult:
        if not self.validation_config.feature_skip_frame:
            return validation_result

        if not validation_result.is_valid:
            self.skip_frame = True
            self.skip_frame_counter = self.validation_config.skip_frame_count
        else:
            if self.skip_frame:
                self.skip_frame_counter -= 1
                self.logger.info(f"Skipping frame. skip_frame_counter: {self.skip_frame_counter}")
                validation_result.is_valid = False
                validation_result.error_code = ErrorCode.SKIP_FRAME
                if self.skip_frame_counter <= 0:
                    self.skip_frame = False
        return validation_result

    def _process(self, image: np.ndarray) -> List:
        """
        Run inference on image.

        @param
            image (np.ndarray): image to be processed
        @return
            boxes (List): list of bounding boxes
        """
        data = {"image": image}
        data = transform(data, self.pre_processors)
        img, shape_list = data
        img = np.expand_dims(img, axis=0)
        shape_list = np.expand_dims(shape_list, axis=0)
        test_in = img.copy()

        output_buffer = self.engine.inference_single(test_in, profiling=False)

        output_shape = list(test_in.shape)
        output_shape[1] = 1
        results = np.reshape(output_buffer[0], output_shape)
        post_proc_results = self.post_process_op(results, shape_list)
        dt_boxes = post_proc_results[0]["points"]

        self.logger.debug(
            f"Bounding boxes detected: {len(dt_boxes)}",
            extra={"custom_dimensions": {"bounding_box": len(dt_boxes)}},
        )

        return dt_boxes

    def run(self, request: TextDetectionRequest) -> TextDetectionResult:
        """
        Run inference on image.

        @param
            request (TextDetectionRequest): request input
        @return
            result (TextDetectionResult): result output
        """

        image = self._pre_process(request.image)
        boxes = self._process(image)
        validation_result = self._post_process(len(boxes))
        return TextDetectionResult(validation_result, boxes, image)
