"""Test src/metrics/ocr_model_metrics.py."""

import unittest
from src.metrics.ocr_model_metrics import OcrModelProcessingMetrics


class TestOcrModelMetrics(unittest.TestCase):
    def test_get_extra_properties(self):
        ocr_model_processing = OcrModelProcessingMetrics(
            "correlation_id",
        )
        ocr_model_processing.set_blob_name("item_name")
        ocr_model_processing.set_edge_inference_metrics(4)
        # ocr_model_processing._set_ocr_metrics(MagicMock(), None)
        properties = ocr_model_processing.getExtraProperties()
        properties = str(properties)
        self.assertTrue(properties.find("correlation_id"))


if __name__ == "__main__":
    unittest.main()
