"""This module is used get/set properties that represent latency at each step in the pipeline.
These will be emitted to Application Insights as custom metrics by the MetricsLogger.
"""


from time import time
from enum import Enum


class LatencyMetrics:
    """This class contains methods which take input params related to latency and returns a
    'properties' object which will be emitted as custom metrics.

    """

    def __init__(self, correlation_id: str) -> None:
        """Initialize the LatencyMetrics class
        @param
            correlation_id(str): Correlation ID for the request
        @return None
        """

        self.correlation_id = correlation_id
        self.transformed_fields = dict()
        self.local_inference_latency = None
        self.ocr_inference_latency = None
        self.tts_inference_latency = None
        self.total_inference_latency = None
        self.outcome_type = OutcomeType.failure.name
        self.is_candidate_for_logging = True

    def getExtraProperties(self) -> dict:
        """
        This function returns properties object which can be used in logging.

        """
        properties = {
            "custom_dimensions": {
                "local_inference_time": self.local_inference_latency,
                "ocr_time": self.ocr_inference_latency,
                "tts_time": self.tts_inference_latency,
                "total_time": self.total_inference_latency,
                "outcome_type": self.outcome_type,
                "correlation_id": self.correlation_id,
                **self.transformed_fields,
            }
        }
        return properties

    def set_edge_inference_metrics(self, start_time: float) -> None:
        """
        Sets the latency values for local text detection step. It is called both when the
        local inference succeeds or when it throws and exception or returns a TextDetectionResult
        with a failure flag.

        @param
            start_time(float): Latency time

        @return
            None
        """
        self.local_inference_latency = time() - start_time

    def set_ocr_metrics(self, start_time: float) -> None:
        """
        Sets the latency values for the OCR call step

        @param
            start_time(float): start time of ocr call

        @return
            None

        """
        self.ocr_inference_latency = time() - start_time

    def set_tts_metrics(self, start_time: float) -> None:
        """
        Sets the latency values for the TTS call step

        @param
            start_time(float): start time of tts call

        @return
            None

        """
        self.tts_inference_latency = time() - start_time

    def set_total_metrics(self, start_time: float) -> None:
        """
        Sets the total latency values metric before exiting the pipeline run for the current
        image frame, e.g. when a duplicate order is detected, TTS call will not be made

        @param
            start_time(float): start time when the pipeline run starts
        @return
            None
        """
        self.total_inference_latency = time() - start_time

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

    def set_meta_data(self, transformed_fields: dict[str, str]) -> None:
        """
        Sets the order type and order number for the current request

        @param
            transformed_fields(dict(str,str)): transformed_fields
        @return
            None
        """
        self.transformed_fields = transformed_fields

    def set_exclude_from_logging(self) -> None:
        """
        Sets the flag to exclude the metrics from logging

        @return
            None
        """
        self.is_candidate_for_logging = False


class OutcomeType(Enum):
    """Error codes that represent the success/failure of the operation

    Args:
        Enum (_type_): outcome value
    """

    success = 1
    failure = 2
    duplicate = 3
    skipped = 4
