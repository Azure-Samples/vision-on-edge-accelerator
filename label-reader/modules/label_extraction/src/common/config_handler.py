"""This module is used to get all configuration and create config objects."""


import ast
import os
from src.pcm.config import ProcessControllerConfig
from src.ocr.config import OCRValidationConfig
from src.edgeinferencing.config import (
    DBPostProcessConfig,
    EdgeModelConfig,
    TextDetectionValidationConfig,
)
from src.frameprocessor.config import LabelExtractionConfig, DuplicateOrderCacheConfig
from src.common.utils import parse_int_from_str
from src.ocr.azureformrecognizer.config import AzureFormRecognizerConfig
from src.tts.az_cogs.config import AzureTTSConfig

from src.frameprovider.config import FrameProviderConfig
from src.tts.model import TTSConfig
from src.frameprocessor.config import StorageConfig, SamplerConfig


class ConfigHandler:
    """
    Get all configuration and create config objects.
    """

    def __init__(self, config_source: str = "environment") -> None:
        """
        Initialize ConfigHandler.

        @param:
            config_source (str): source of all configurations
        """
        self.config_source = config_source

    def get_frame_provider_config(self) -> FrameProviderConfig:
        """
        Get FrameProviderConfig object.

        @return:
            FrameProviderConfig (object): FrameProviderConfig class
        """
        return FrameProviderConfig(
            frame_rate_ui=int(self.get_config("FRAME_RATE_UI")),
            frame_size_ui=ast.literal_eval(self.get_config("FRAME_SIZE_UI")),
            frame_size_queue=ast.literal_eval(self.get_config("FRAME_SIZE_QUEUE")),
            camera_path=parse_int_from_str(self.get_config("CAMERA_PATH")),
            vid_stream_internal_url=self.get_config("VID_STREAM_INTERNAL_URL"),
            frame_rate_camera=int(self.get_config("FRAME_RATE_CAMERA")),
        )

    def get_az_cogs_tts_config(self) -> AzureTTSConfig:
        """
        Get TtsConfig singleton instance. Ensures env variables in the module are read only once

        @return:
            AzureTTSConfig (object): AzureTTSConfig class
        """

        return AzureTTSConfig(
            self.get_config("AZURE_COGNITIVE_SERVICE_SPEECH_KEY"),
            self.get_config("AZURE_COGNITIVE_SERVICE_SPEECH_ENDPOINT"),
            ast.literal_eval(self.get_config("AZURE_COGNITIVE_SERVICE_SPEECH_TIMEOUT")),
        )

    def get_tts_config(self) -> TTSConfig:
        """
        Get TTS Config

        @returns
            TTSConfig (object): TTSConfig class
        """
        return TTSConfig(
            speech_synthesis_voice_name=self.get_config("SPEECH_SYNTHESIS_VOICE_NAME"),
            speech_synthesis_language=self.get_config("SPEECH_SYNTHESIS_LANGUAGE"),
            speech_synthesis_style=self.get_config("SPEECH_SYNTHESIS_STYLE"),
            speech_synthesis_profile_rate=self.get_config(
                "SPEECH_SYNTHESIS_PROFILE_RATE"
            ),
            speech_synthesis_profile_pitch=self.get_config(
                "SPEECH_SYNTHESIS_PROFILE_PITCH"
            ),
        )

    def get_az_cogs_formrecog_config(self) -> AzureFormRecognizerConfig:
        """
        Get AzureFormRecognizerConfig singleton instance. Ensures env variables in the module are read only once

        @return:
            AzureFormRecognizerConfig (object): AzureFormRecognizerConfig class
        """

        return AzureFormRecognizerConfig(
            self.get_config("AZURE_COGNITIVE_SERVICE_FORMRECOG_KEY"),
            self.get_config("AZURE_COGNITIVE_SERVICE_FORMRECOG_ENDPOINT"),
            self.get_config("AZURE_COGNITIVE_SERVICE_FORMRECOG_MODEL_ID"),
        )

    def get_db_postprocess_config(self) -> DBPostProcessConfig:
        """
        Get DBPostProcessConfig.

        @return:
            DBPostProcessConfig (object): DBPostProcessConfig class
        """
        return DBPostProcessConfig(
            thresh=float(self.get_config("EDGE_MODEL_DB_THRESHOLD")),
            box_thresh=float(self.get_config("EDGE_MODEL_DB_BOX_THRESHOLD")),
            max_candidates=int(self.get_config("EDGE_MODEL_DB_MAX_CANDIDATE")),
            unclip_ratio=int(self.get_config("EDGE_MODEL_DB_UNCLIP_RATIO")),
            use_dilation=bool(self.get_config("EDGE_MODEL_DB_USE_DILATION")),
            score_mode=self.get_config("EDGE_MODEL_DB_SCORE_MODE"),
        )

    def get_edge_model_config(self) -> EdgeModelConfig:
        """
         Get EdgeModelConfig.

        @return:
            EdgeModelConfig (object): EdgeModelConfig class
        """
        return EdgeModelConfig(
            original_model_path=self.get_config("EDGE_MODEL_LOCAL_PATH"),
            image_size=ast.literal_eval(self.get_config("FRAME_SIZE_EDGE_MODEL")),
        )

    def get_text_detection_validation_config(self) -> TextDetectionValidationConfig:
        """
        Get TextDetectionValidationConfig.

        @return:
            TextDetectionValidationConfig (object): TextDetectionValidationConfig class
        """
        return TextDetectionValidationConfig(
            bounding_box_threshold_low=int(
                self.get_config("TEXT_DETECTION_VALIDATION_BOUNDING_BOX_THRESHOLD_LOW")
            ),
            bounding_box_threshold_label=int(
                self.get_config(
                    "TEXT_DETECTION_VALIDATION_BOUNDING_BOX_THRESHOLD_LABEL"
                )
            ),
            feature_skip_frame=bool(self.get_config("FEATURE_SKIP_FRAME")),
            skip_frame_count=int(
                self.get_config("TEXT_DETECTION_VALIDATION_SKIP_FRAME_COUNT")
            ),
        )

    def get_label_extraction_config(self) -> LabelExtractionConfig:
        """
        Get LabelExtractionConfig.

        @return:
            LabelExtractionConfig (object): LabelExtractionConfig class
        """
        return LabelExtractionConfig(
            frame_size_ocr=ast.literal_eval(self.get_config("FRAME_SIZE_OCR")),
            status_internal_url=self.get_config("STATUS_INTERNAL_URL"),
            order_info_internal_url=self.get_config("ORDER_INFO_INTERNAL_URL"),
            store_id=self.get_config("STORE_ID"),
            device_id=os.environ.get("IOTEDGE_DEVICEID", "LOCALHOST"),
        )

    def get_ocr_validation_config(self) -> OCRValidationConfig:
        """
        Get OCRValidationConfig.

        @return:
            OCRValidationConfig (object): OCRValidationConfig class
        """
        return OCRValidationConfig(
            confidence_threshold=float(self.get_config("OCR_CONFIDENCE_THRESHOLD")),
        )

    def get_storage_config(self) -> StorageConfig:
        """
        Get StorageConfig singleton instance. Ensures env variables in the module are read only once

        @return:
            StorageConfig (object): StorageConfig class
        """
        return StorageConfig(
            self.get_config("BLOB_STORAGE_CONN_STRING"),
            self.get_config("AZURE_BLOB_STORAGE_CONTAINER_NAME"),
        )

    def get_sampler_config(self) -> SamplerConfig:
        """
        Get StorageConfig singleton instance. Ensures env variables in the module are read only once

        @return:
            StorageConfig (object): StorageConfig class
        """
        return SamplerConfig(int(self.get_config("NUM_IMAGES_CAP_PER_HOUR")))

    def get_duplicate_order_cache_config(self) -> DuplicateOrderCacheConfig:
        """
        Get DuplicateOrderCacheConfig.

        @return:
            DuplicateOrderCacheConfig (object): DuplicateOrderCacheConfig class
        """
        return DuplicateOrderCacheConfig(
            max_len=ast.literal_eval(
                self.get_config("DUPLICATE_ORDER_CACHE_MAX_LENGTH")
            ),
            max_age_in_seconds=ast.literal_eval(
                self.get_config("DUPLICATE_ORDER_CACHE_MAX_AGE_IN_SECONDS")
            ),
        )

    def get_process_conroller_config(self) -> ProcessControllerConfig:
        return ProcessControllerConfig(
            admin_internal_url=self.get_config("ADMIN_INTERNAL_URL"),
        )

    def get_config(self, config_name: str) -> str:
        """
        Get value of a specific configuration parameter.

        @return:
            value (str): Parameter value
        """
        if self.config_source == "environment":
            return self._read_env_variable(config_name)
        else:
            raise ValueError(f"Unknown config source: {self.config_source}")

    def _read_env_variable(self, config_name) -> str:
        """
        Read environment variable.

        @param:
            config_name (str): Name of the configuration parameter
        @return:
            value (str): Parameter value
        """
        value = os.environ.get(config_name)
        if value is None:
            raise ValueError(f"Config environment variable {config_name} is not set.")
        return value
