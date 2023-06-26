from logging import Logger

from azure.ai.formrecognizer import AnalyzeResult
from src.ocr.model import OrderLabelFieldInfo
from src.ocr.transformer import OcrResultTransformer
from src.common.status import ErrorCode
from src.validators.ocr_validator import OcrValidationResult, OcrResultValidator


class LabelProcessor:
    """
    Class to process label information
    """

    def __init__(self, confidence_threshold: float, logger: Logger) -> None:
        """
        Initialize the class

        @param
            confidence_threshold (float): threshold for field level confidence
            logger (Logger): logger
        """
        self._logger = logger
        self.confidence_threshold = confidence_threshold
        self._ocr_validator = OcrResultValidator(self.confidence_threshold, logger)
        self._ocr_transformer = OcrResultTransformer()

    def extract_fields(
        self, ocr_result: AnalyzeResult
    ) -> dict[str, OrderLabelFieldInfo]:
        """
        Extract fields from Azure Form Recognizer result

        @param
            ocr_result (AnalyzeResult): Azure Form Recognizer result
            fields (dict[str, dict]): fields to extract from Azure Form Recognizer result
        @return
            dict[str, OrderLabelFieldInfo]: Dictionary of extracted field names along with field
            information such as value and confidence
        """
        extracted_fields = {}
        for idx, analyzed_document in enumerate(ocr_result.documents):
            for field_name, field_info in analyzed_document.fields.items():
                field_value = (
                    field_info.value if field_info.value else field_info.content
                )
                extracted_fields[field_name] = OrderLabelFieldInfo(
                    field_name, field_value, field_info.confidence
                )
        return extracted_fields

    def validate_fields(
        self, extracted_fields: dict[str, OrderLabelFieldInfo]
    ) -> OcrValidationResult:
        """
        Validate extracted fields

        @param
            extracted_fields (dict[str, OrderLabelFieldInfo]): Dictionary of extracted field names along with
            field information such as value and confidence
        @return
            OCRValidationResult: validation result with status and error code
        """
        if not extracted_fields:
            return OcrValidationResult(False, ErrorCode.FIELD_MISSING)

        for field_name, field_info in extracted_fields.items():
            validation_result = self._ocr_validator.validate_field_is_empty(field_info)
            if not validation_result.is_valid:
                return validation_result

            validation_result = self._ocr_validator.validate_field_confidence(
                field_info
            )
            if not validation_result.is_valid:
                return validation_result
        return OcrValidationResult(True, None)

    def transform_fields(
        self, validated_fields: dict[str, OrderLabelFieldInfo]
    ) -> dict[str, str]:
        """
        Transform validated fields as per business requirement

        @param
            validated_fields (dict[str, OrderLabelFieldInfo]): Dictionary of extracted field names along with field
            information such as value and confidence
        @return
            dict[str, str]: Dictionary of field names and their transformed values
        """
        transformed_fields = {}
        for field_name, field_info in validated_fields.items():
            transformed_fields[field_name] = self._ocr_transformer.transform_field_for_tts(field_info)
        return transformed_fields

    def hash_identity(self, transformed_fields: dict[str, str]) -> str:
        """
        Generate hash identity for the label

        @param
            transformed_fields (dict[str, str]): Dictionary of field names and their transformed values
        @return
            str: Hashed identity of the label
        """
        return hash(frozenset(transformed_fields.items()))

    def order_notification(self, transformed_fields: dict[str, str]) -> dict[str, str]:
        """
        Generate order notification using the transformed fields

        @param
            transformed_fields (dict[str, str]): Dictionary of field names and their transformed values
        @return
            dict[str, str]: Dictionary of field names and their values to be sent as notification to UI
        """
        return transformed_fields

    def narrate_content(self, transformed_fields: dict[str, str]) -> dict[str, str]:
        """
        Generate narrat using the transformed fields

        @param
            transformed_fields (dict[str, str]): Dictionary of field names and their transformed values
        @return
            dict[str, str]: Dictionary of field names and their values to be sent as notification to UI
        """
        return transformed_fields
