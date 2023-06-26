from logging import Logger
from typing import Union
from src.frameprocessor.labelprocessor.model import (
    LabelProcessingRequest,
    LabelProcessingResponse,
)
from src.frameprocessor.labelprocessor.default_label_processor import LabelProcessor
from src.frameprocessor.labelprocessor.afr_runner import AFRRunner
from src.ocr.model import OrderLabelFieldInfo
from src.validators.ocr_validator import OcrValidationResult


class LabelProcessing:
    """
    Class to orchestrate label processing pipeline.
    """

    def __init__(
        self,
        afr_runner: AFRRunner,
        label_processor: LabelProcessor,
        logger: Logger,
    ):
        self.afr_runner = afr_runner
        self._label_processor = label_processor
        self._logger = logger

    def _build_label_processing_response(
        self,
        extracted_result: dict[str, OrderLabelFieldInfo],
        validated_result: OcrValidationResult,
        transformed_result: Union[dict[str, str], None],
    ):
        """
        Builds the LabelProcessingResponse object

        @param
            extracted_result (dict[str, OrderLabelFieldInfo]): dict extracted by Azure Form Recognizer
            validated_result (OcrValidationResult): result of field Validation
            transformed_result (Union[dict[str, str], None]): dict post transforming the string
        @return
            ocr_response (OcrResponse): label processing response
        """

        if validated_result.is_valid:
            hash_identity = self._label_processor.hash_identity(transformed_result)
            content_for_narration = self._label_processor.narrate_content(
                transformed_result
            )
            content_for_ui = self._label_processor.order_notification(
                transformed_result
            )
            return LabelProcessingResponse(
                extracted_result,
                validated_result,
                transformed_result,
                hash_identity,
                content_for_narration,
                content_for_ui,
            )
        else:
            return LabelProcessingResponse(
                extracted_result, validated_result, None, None, None, None
            )

    def run(self, request: LabelProcessingRequest) -> LabelProcessingResponse:
        """
        Run the label processing and returns a response

        @param
            request (LabelProcessingRequest): label processing request
        @return
            ocr_response (OcrResponse): label processing response
        """

        afr_result = self.afr_runner.run(request)

        if afr_result is None:
            self._logger.error(
                "Error while running Azure form recognizer, no response from AFR"
            )
            raise Exception(
                "Error while running Azure form recognizer, no response from Azure form recognizer"
            )

        extracted_result = self._label_processor.extract_fields(afr_result)

        validated_result = self._label_processor.validate_fields(extracted_result)

        transformed_result = None

        if validated_result.is_valid:
            transformed_result = self._label_processor.transform_fields(
                extracted_result
            )

        return self._build_label_processing_response(
            extracted_result, validated_result, transformed_result
        )
