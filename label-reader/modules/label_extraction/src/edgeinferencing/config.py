"""This module is used to provide the configurations for edge text detection."""
from typing import List


class EdgeInferencingPreProcessConfig:
    """
    Configurations class for edge inferencing pre-prossing pipeline.
    """

    def __init__(self) -> None:
        """
        Initialize the configuration.
        """
        self.det_resize_for_test = {}
        self.normalize_image = {
            "std": [0.229, 0.224, 0.225],
            "mean": [0.485, 0.456, 0.406],
            "scale": 1.0 / 255.0,
            "order": "hwc",
        }
        self.to_chw_image = None
        self.keep_keys = {"keep_keys": ["image", "shape"]}


class EdgeModelConfig:
    """
    Class for edge model configurations.
    """

    def __init__(self, original_model_path: str, image_size: List) -> None:
        """
        Initialize the configuration.

        @param
            original_model_path (str): path to the ONNX model
            image_size (List): image size as [height, width]
        """
        self.original_model_path = original_model_path
        self.image_size = image_size
        self.fp16 = True
        self.dynamic_shape = True
        self.profile_config = [
            {"x": [(1, 3, 960, 960), (1, 3, 1280, 1280), (1, 3, 1536, 1536)]}
        ]


class DBPostProcessConfig:
    """
    Configurations class for edge inferencing post-prossing.
    """

    def __init__(
        self,
        thresh: float,
        box_thresh: float,
        max_candidates: int,
        unclip_ratio: int,
        use_dilation: bool,
        score_mode: str,
    ) -> None:
        """
        Initialize the configuration.

        @param
            thresh (float): threshold for nms
            box_thresh (float): threshold for box, this can be adjusted as per environmental conditions
            max_candidates (int): max candidates for nms
            unclip_ratio (int): ratio for unclip
            use_dilation (bool): whether to use dilation
            score_mode (str): score mode
        """
        self.thresh = thresh
        self.box_thresh = box_thresh
        self.max_candidates = max_candidates
        self.unclip_ratio = unclip_ratio
        self.use_dilation = use_dilation
        self.score_mode = score_mode


class TextDetectionValidationConfig:
    """
    Class for edge model inferencing result validation configurations.
    """

    def __init__(
        self,
        bounding_box_threshold_low: int,
        bounding_box_threshold_label: int,
        feature_skip_frame: bool,
        skip_frame_count: int,
    ):
        """
        Initialize the configuration.

        @param
            bounding_box_threshold_low (int): threshold for low confidence bounding box
                                                    (minimum count of text boxes to notify low bounding box)
            bounding_box_threshold_label (int): threshold for label confidence bounding box
                                                    (required count of text boxes to qualify a label as valid label)
            feature_skip_frame (bool): feature flag to enable skipping frames
            skip_frame_count (int): number of frames to skip when feature is available
        """
        self.bounding_box_threshold_low = bounding_box_threshold_low
        self.bounding_box_threshold_label = bounding_box_threshold_label
        self.feature_skip_frame = feature_skip_frame
        self.skip_frame_count = skip_frame_count
