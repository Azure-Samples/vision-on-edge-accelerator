"""Test src/common/test_expiring_cache.py."""

import unittest

from src.common.app_logger import get_disabled_logger
from src.common.expiring_cache import ExpiringCache
import time
from unittest.mock import patch


class TestExpiringCache(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.logger = get_disabled_logger().get_logger()

    def test_add_item(self):
        duplicate_order_cache = ExpiringCache(
            max_len=5, max_age_in_seconds=100, logger=self.logger
        )
        duplicate_order_cache.initialize()

        duplicate_order_cache.add_item("order1", "order1")
        value = duplicate_order_cache.get_value("order1")
        self.assertEqual(value, "order1")

        duplicate_order_cache.add_item("order2", "order2")
        duplicate_order_cache.add_item("order3", "order3")
        len = duplicate_order_cache.get_len()
        self.assertEqual(len, 3)

    def test_add_item_more_than_len(self):
        duplicate_order_cache = ExpiringCache(
            max_len=5, max_age_in_seconds=100, logger=self.logger
        )
        duplicate_order_cache.initialize()

        duplicate_order_cache.add_item("order1", "order1")
        duplicate_order_cache.add_item("order2", "order2")
        duplicate_order_cache.add_item("order3", "order3")
        duplicate_order_cache.add_item("order4", "order4")
        duplicate_order_cache.add_item("order5", "order5")
        len = duplicate_order_cache.get_len()
        self.assertEqual(len, 5)

        duplicate_order_cache.add_item("order6", "order6")
        len = duplicate_order_cache.get_len()
        self.assertEqual(len, 5)

    def test_remove_item(self):
        duplicate_order_cache = ExpiringCache(
            max_len=5, max_age_in_seconds=100, logger=self.logger
        )
        duplicate_order_cache.initialize()

        duplicate_order_cache.remove("order5")
        len = duplicate_order_cache.get_len()
        self.assertEqual(len, 0)

        duplicate_order_cache.add_item("order1", "order1")
        value = duplicate_order_cache.get_value("order1")
        self.assertEqual(value, "order1")

        duplicate_order_cache.add_item("order2", "order2")
        duplicate_order_cache.add_item("order3", "order3")
        len = duplicate_order_cache.get_len()
        self.assertEqual(len, 3)

        duplicate_order_cache.remove("order1")
        len = duplicate_order_cache.get_len()
        self.assertEqual(len, 2)

        duplicate_order_cache.remove("order2")
        len = duplicate_order_cache.get_len()
        self.assertEqual(len, 1)

        duplicate_order_cache.remove("order3")
        len = duplicate_order_cache.get_len()
        self.assertEqual(len, 0)

        duplicate_order_cache.remove("order4")
        len = duplicate_order_cache.get_len()
        self.assertEqual(len, 0)

    def test_clear_cache(self):
        duplicate_order_cache = ExpiringCache(
            max_len=5, max_age_in_seconds=100, logger=self.logger
        )
        duplicate_order_cache.initialize()
        duplicate_order_cache.add_item("order1", "order1")

        value = duplicate_order_cache.get_value("order10")
        self.assertEqual(value, None)

        value = duplicate_order_cache.get_value("order1")
        self.assertEqual(value, "order1")

        duplicate_order_cache.add_item("order2", "order2")
        duplicate_order_cache.add_item("order3", "order3")
        len = duplicate_order_cache.get_len()
        self.assertEqual(len, 3)

        duplicate_order_cache.clear()
        len = duplicate_order_cache.get_len()
        self.assertEqual(len, 0)

    def test_contains_cache(self):
        duplicate_order_cache = ExpiringCache(
            max_len=5, max_age_in_seconds=100, logger=self.logger
        )
        duplicate_order_cache.initialize()

        duplicate_order_cache.add_item("order1", "order1")
        value = duplicate_order_cache.contains("order1")
        duplicate_order_cache.add_item("order2", "order2")
        duplicate_order_cache.add_item("order3", "order3")
        self.assertEqual(value, True)

        value = duplicate_order_cache.contains("order10")
        self.assertEqual(value, False)

        value = duplicate_order_cache.contains("order2")
        self.assertEqual(value, True)

    def test_expiring_cache(self):
        duplicate_order_cache = ExpiringCache(
            max_len=5, max_age_in_seconds=1, logger=self.logger
        )
        duplicate_order_cache.initialize()
        duplicate_order_cache.add_item("order1", "order1")
        time.sleep(2)
        value = duplicate_order_cache.contains("order1")
        self.assertEqual(value, False)

        duplicate_order_cache.add_item("order2", "order2")
        duplicate_order_cache.add_item("order3", "order3")
        value = duplicate_order_cache.contains("order10")
        self.assertEqual(value, False)

        value = duplicate_order_cache.contains("order2")
        self.assertEqual(value, True)

    @patch(
        "src.common.expiring_cache.ExpiringCache.initialize",
        side_effect=Exception("test"),
    )
    def test_expiring_cache_exception(self, _):
        duplicate_order_cache = ExpiringCache(
            max_len=5, max_age_in_seconds=1, logger=self.logger
        )
        with self.assertRaises(Exception):
            duplicate_order_cache.initialize()


if __name__ == "__main__":
    unittest.main()
