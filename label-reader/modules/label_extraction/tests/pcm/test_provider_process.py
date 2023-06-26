import unittest
from unittest.mock import patch
from src.pcm.provider_process import FrameProviderProcess


class TestFrameProviderProcess(unittest.TestCase):
    @patch("src.frameprovider.camera_integration.ConfigHandler")
    @patch(
        "src.frameprovider.camera_integration.CameraIntegration.start_camera",
        return_value=True,
    )
    @patch("src.pcm.provider_process.os")
    def test_frame_provider_process_run_method(self, *args):
        fp = FrameProviderProcess()
        try:
            fp.run(None)
        except Exception as e:
            self.fail(e)
        self.assertTrue(True)
