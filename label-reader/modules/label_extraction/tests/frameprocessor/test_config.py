import unittest
from src.frameprocessor.config import LabelExtractionConfig, DuplicateOrderCacheConfig


class TestLabelExtractionConfig(unittest.TestCase):
    def test_LabelExtractionConfig_init_with_default_values(self):
        config = LabelExtractionConfig((480, 640), "", "", "", "")
        self.assertEqual(config.frame_size_ocr[0], 480)
        self.assertEqual(config.frame_size_ocr[1], 640)
        self.assertEqual(config.status_internal_url, "")
        self.assertEqual(config.order_info_internal_url, "")

    def test_DuplicateOrderCacheConfig_init_with_default_values(self):
        config = DuplicateOrderCacheConfig(100, 10)
        self.assertEqual(config.max_len, 100)
        self.assertEqual(config.max_age_in_seconds, 10)
