import unittest
from src.frameprovider.config import FrameProviderConfig


class TestFrameProviderConfig(unittest.TestCase):
    def test_FrameProviderConfig_init_with_default_values(self):
        config = FrameProviderConfig(30, (640, 480), (640, 480), 0, "", 15)
        self.assertEqual(config.frame_rate_ui, 30)
        self.assertEqual(config.frame_size_ui, (640, 480))
        self.assertEqual(config.frame_size_queue, (640, 480))
        self.assertEqual(config.camera_path, 0)
        self.assertEqual(config.vid_stream_socket_url, "")
        self.assertEqual(config.frame_rate_camera, 15)
