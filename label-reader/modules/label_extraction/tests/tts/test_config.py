# Standard library imports...

from unittest.mock import patch
import unittest
from src.tts.az_cogs.config import AzureTTSConfig


class TestConfig(unittest.TestCase):
    @patch("requests.post")
    def test_success_path(self, mock_post):
        print("------ Running Unit Test - initialize config -------")
        l_tts_config = AzureTTSConfig("dummy", "dummy url", None)
        self.assertEqual(l_tts_config.l_subscription_key, "dummy")
        self.assertEqual(l_tts_config.l_cogs_tts_endpoint, "dummy url")
        print("------ Success! Running Unit Test - initialize config -------")


if __name__ == "__main__":
    unittest.main()
