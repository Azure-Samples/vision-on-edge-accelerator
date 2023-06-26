# import time

import logging
from src.ocr.azureformrecognizer.config import AzureFormRecognizerConfig

from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import AnalyzeResult, DocumentAnalysisClient

logging.getLogger("azure.core.pipeline.policies.http_logging_policy").setLevel(
    logging.WARNING
)


class AzureFormRecognizer:
    """Implements the call to Azure Cognitive Services - Form Recognizer"""

    def __init__(
        self, config: AzureFormRecognizerConfig, logger: logging.Logger
    ) -> None:
        """Initialize the Form Recognizer configurations and the logger utility
        Raises:
            ValueError when the configs cannot be read from environment variables
        """

        # Initialize the logger utility
        self.l_logger = logger

        # Initialize the Form Recognizer configurations
        self.l_config = config

        # Initialize the Form Recognizer client
        self.document_analysis_client = DocumentAnalysisClient(
            endpoint=self.l_config.l_cogs_formrecog_endpoint,
            credential=AzureKeyCredential(self.l_config.l_cogs_formrecog_key),
        )

    def run(self, img_payload: bytes) -> AnalyzeResult:
        """Externally callable method that returns the fields extracted by Azure Form Recognizer Service from the input image.
        Args:
            img_payload (bytes): the image byte stream from which fields must be extracted by Azure Form Recognizer

        Returns:
            AnalyzeResult: Document analysis result from Azure Form Recognizer
        """

        # # call the OCR API and get back an operation ID to track ocr completion
        # operation_id = self._get_ocr_operation_id(img_payload)

        # # use the operation id to get back the OCR Results using a GET operation
        # return self._get_ocr_results(operation_id)

        poller = self.document_analysis_client.begin_analyze_document(
            model_id=self.l_config.l_cogs_formrecog_model_id, document=img_payload
        )
        return poller.result()
