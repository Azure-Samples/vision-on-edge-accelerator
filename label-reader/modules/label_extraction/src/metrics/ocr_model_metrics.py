from enum import Enum
from src.frameprocessor.labelprocessor.model import LabelProcessingResponse
from src.common.status import ErrorCode
from src.validators.ocr_validator import OcrValidationResult


"""This module is used get & set properties for ocr model
    metrics that would be added as custom dimensions and logged to Application Insights
"""


class OcrModelProcessingMetrics:
    """This class contains methods which take some input params related to ocr
    model processing and returns properties object which can be used in logging.

    """

    def __init__(self, correlation_id: str) -> None:

        """Initialize the OcrModelProcessingMetrics class with default values.

        @param
            correlation_id(str): correlation id of the image frame containing the label on the coffee cup
        """
        self.correlation_id = correlation_id
        self.evaluation_type = "system"
        self.failure_cause = None
        self.frame_blob_id = None
        self.outcome_type = OutcomeType.failure.name
        self.edge_model_num_bboxes = None
        self.is_candidate_for_logging = True

    def set_edge_inference_metrics(self, num_bboxes: int) -> None:
        """
        Set the latency metrics for edge inference.

        @param
            num_bboxes(int): number of bounding boxes returned by edge inference
        @return: None
        """
        self.edge_model_num_bboxes = num_bboxes

    def set_blob_name(self, blob_name: str) -> None:
        """Set the blob name of the image frame uploaded to Blob storage in the latency metric
        @param
            blob_name(str): blob name of the image frame uploaded to Blob storage
        @return: None
        """
        self.frame_blob_id = blob_name

    def getExtraProperties(
        self,
    ) -> None:
        """ "
        This function returns properties object which will be emitted to App Insights as custom metrics.

        """
        properties = {
            "custom_dimensions": {
                "evaluation_type": self.evaluation_type,
                "edge_model_num_bboxes": self.edge_model_num_bboxes,
                "outcome_type": self.outcome_type,
                "frame_blob_id": self.frame_blob_id,
                "failure_cause": self.failure_cause,
                "correlation_id": self.correlation_id,
            }
        }
        return properties

    def set_exclude_from_logging(self) -> None:
        """
        Sets the flag to exclude the metrics from logging

        @return
            None
        """
        self.is_candidate_for_logging = False

    def set_outcome_type(self, outcome_type: str) -> None:
        """
        Sets the total latency values metric before exiting the pipeline run for the current
        image frame, e.g. when a duplicate order is detected, TTS call will not be made

        @param
            outcome_type(OutcomeType): OutcomeType enum
        @return
            None
        """
        self.outcome_type = outcome_type


class OutcomeType(Enum):
    """Error codes that represent the success/failure of the operation

    Args:
        Enum (_type_): outcome value
    """

    success = 1
    failure = 2


def set_ocr_model_metrics(
    ocr_result: LabelProcessingResponse,
    ds_model_metrics: OcrModelProcessingMetrics,
):
    """
    Set the model metrics for ocr.

    @param
        ds_model_metrics (DsModelMetrics): ds model metrics
        ocr_result (OcrResponse): ocr result
        trace_logger (Logger): logger object to log application telemetry to Application Insights

    @return
        None
    """

    ds_model_metrics.set_outcome_type(OutcomeType.failure.name)
    ds_model_metrics.failure_cause = ErrorCode.OCR_ERROR

    if ocr_result is not None:
        set_ocr_validation_on_ds_metrics(ds_model_metrics, ocr_result.validation_result)


def set_ocr_validation_on_ds_metrics(
    ds_model_metrics: OcrModelProcessingMetrics, validation_result: OcrValidationResult
):
    if validation_result is None or not validation_result.is_valid:
        ds_model_metrics.set_outcome_type(OutcomeType.failure.name)
        ds_model_metrics.failure_cause = (
            validation_result.error_code or ErrorCode.OCR_ERROR
        )
        return

    ds_model_metrics.set_outcome_type(OutcomeType.success.name)
    ds_model_metrics.failure_cause = None
