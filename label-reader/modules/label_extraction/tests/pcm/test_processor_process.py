import unittest
from unittest.mock import MagicMock, Mock, patch
from src.pcm.processor_process import FrameProcessorProcess


class TextDetectionMock(MagicMock):
    __name__ = "TextDetectionMock"


class OCRMock(MagicMock):
    __name__ = "OCRMock"


class LabelProcessingMock(MagicMock):
    __name__ = "LabelProcessingMock"


class TTSMock(MagicMock):
    __name__ = "TTSMock"


class TestFrameProcessorProcess(unittest.TestCase):
    @patch("src.frameprocessor.label_extraction.ConfigHandler")
    @patch("src.frameprocessor.label_extraction.SocketClient")
    @patch(
        "src.frameprocessor.label_extraction.TextDetection",
        new_callable=TextDetectionMock,
    )
    @patch(
        "src.frameprocessor.labelprocessor.label_processing",
        new_callable=LabelProcessingMock,
    )
    @patch(
        "src.frameprocessor.label_extraction.TTS",
        new_callable=TTSMock,
    )
    @patch("time.sleep", side_effect=InterruptedError("test"))
    @patch("src.frameprocessor.label_extraction.encode_audio")
    @patch("src.frameprocessor.label_extraction.encode_image")
    @patch("src.frameprocessor.label_extraction.OrderNotifier")
    @patch("src.metrics.latency_metrics.LatencyMetrics.set_tts_metrics")
    @patch("src.metrics.latency_metrics.LatencyMetrics.set_edge_inference_metrics")
    @patch("src.frameprocessor.label_extraction.convert_to_jpeg")
    @patch("src.common.sampler.BasicSampler")
    @patch("src.frameprocessor.label_extraction.ExpiringCache")
    @patch("src.metrics.latency_metrics.LatencyMetrics.set_total_metrics")
    @patch("src.pcm.processor_process.os")
    def test_frame_processor_process_run_method(self, *args):
        fp = FrameProcessorProcess()
        queue = Mock()
        queue.is_empty.side_effect = [False, True]
        try:
            fp.run(queue)
        except InterruptedError:
            queue.get_item.assert_called_once()
