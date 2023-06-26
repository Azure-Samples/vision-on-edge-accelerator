"""Test src/metrics/latency_metrics.py."""

import unittest
from time import time
from src.metrics.latency_metrics import LatencyMetrics


class TestLatencyMetrics(unittest.TestCase):
    def test_get_extra_properties(self):
        latency_metrics = LatencyMetrics("correlation_id")
        latency_metrics.set_edge_inference_metrics(time())
        latency_metrics.set_ocr_metrics(time())
        latency_metrics.set_tts_metrics(time())
        properties = latency_metrics.getExtraProperties()
        properties = str(properties)
        self.assertTrue(properties.find("local_inference_outcome"))


if __name__ == "__main__":
    unittest.main()
