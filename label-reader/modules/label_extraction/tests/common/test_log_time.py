"""Test src/util/test_log_time."""

import unittest
from src.common.log_time import log_time, _create_properties


class TestLogTime(unittest.TestCase):
    def test_log_time(self):
        @log_time
        def test_func(msg):
            return msg

        self.assertEqual(test_func("hello"), "hello")

    def test_create_properties(self):
        def test_func(msg):
            return msg

        properties = str(_create_properties(test_func, 1))
        self.assertTrue(properties.find("test_log_time.py"))


if __name__ == "__main__":
    unittest.main()
