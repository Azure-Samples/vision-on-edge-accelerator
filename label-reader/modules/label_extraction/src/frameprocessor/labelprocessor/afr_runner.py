"""This module is used to provide the Azure form recognizer implementation."""
import io
from logging import getLogger
from typing import List, Union
import numpy as np
from azure.ai.formrecognizer import AnalyzeResult
import cv2

from src.common.utils import convert_to_jpeg
from src.ocr.exception import OcrProcessException
from src.frameprocessor.labelprocessor.model import (
    LabelProcessingRequest,
)
from src.ocr.azureformrecognizer.config import AzureFormRecognizerConfig
from src.ocr.azureformrecognizer.azure_form_recognizer import AzureFormRecognizer


class AFRRunner:
    """
    Class for pre, process and post processing of ocr
    """

    def __init__(
        self,
        frame_size: List,
        az_formrecog_config: AzureFormRecognizerConfig,
    ) -> None:
        """
        Initialize the class

        @param
            frame_size (List): frame size
            az_formrecog_config (AzureOcrConfig): azure form recognizer config
        """
        self.logger = getLogger("azure_form_recognizer")
        self._ocr = AzureFormRecognizer(az_formrecog_config, self.logger)

        self._frame_size = frame_size

        self._encoding = "utf-8-sig"

    def _pre_process(self, img_payload: np.ndarray) -> np.ndarray:
        """
        Pre process the image (resize image)

        @param
            img_payload (np.ndarray): image payload
        @return
            img_payload (np.ndarray): image payload pre processed
        """
        return cv2.resize(img_payload, self._frame_size)

    def _process(self, img_payload: np.ndarray) -> Union[AnalyzeResult, None]:
        """
        Process the image (call azure ocr)

        @param
            img_payload (np.ndarray): image payload
        @return
            ocr_result (Union[ReadResult, None]): ocr result or None
        """
        try:
            return self._ocr.run(io.BytesIO(convert_to_jpeg(img_payload)))
        except Exception as e:
            self.logger.error(f"Error in Azure form recognizer Call: {e}")
            self.logger.exception(e)
            raise OcrProcessException(
                f"Azure form recognizer Process failed {e}", e
            ) from e

    def run(self, request: LabelProcessingRequest) -> Union[AnalyzeResult, None]:
        """
        Run the ocr process (pre, process and post process)

        @param
            request (OcrRequest): ocr request
        @return
            ocr_response (OcrResponse): ocr response
        """
        img = self._pre_process(request.image)
        return self._process(img)
