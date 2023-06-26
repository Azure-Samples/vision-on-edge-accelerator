"""Test src/util/test_log_time."""

import unittest
from unittest.mock import MagicMock
from src.common.metrics_logger import MetricsLogger
from src.metrics.ocr_model_metrics import OcrModelProcessingMetrics
from src.metrics.latency_metrics import LatencyMetrics


class TestMetricsLogger(unittest.TestCase):
    def test_log_latency_metics_error(self):
        m_logger = MetricsLogger(MagicMock())
        l_metrics_data = LatencyMetrics("dummy")
        self.assertRaises(
            Exception,
            m_logger.log_latency_metrics,
            l_metrics_data.getExtraProperties(),
            None,
        )

    def test_log_ds_metics_error(self):
        m_logger = MetricsLogger(MagicMock())
        l_metrics_data = OcrModelProcessingMetrics(
            "dummy",
        )
        self.assertRaises(
            Exception,
            m_logger.log_ds_model_metrics,
            l_metrics_data.getExtraProperties(),
            None,
        )
