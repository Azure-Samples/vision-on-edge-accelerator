import multiprocessing
import time
import unittest
from unittest.mock import MagicMock, patch
from src.pcm.controller import ProcessController


def mock_start_camera():
    while True:
        time.sleep(1)


class TestController(unittest.TestCase):
    @patch(
        "src.common.config_handler.ConfigHandler.get_frame_provider_config",
        return_value=MagicMock(),
    )
    @patch(
        "src.frameprovider.camera_integration.CameraIntegration.start_camera",
        side_effect=mock_start_camera,
    )
    @patch("src.pcm.controller.ConfigHandler")
    @patch("src.pcm.controller.SocketClient")
    @patch("src.pcm.processor_process.os")
    @patch("src.pcm.provider_process.os")
    def test_controller_start_when_processes_are_not_running(self, *args):
        """Test to start processes."""
        multiprocessing_context = multiprocessing.get_context()
        controller = ProcessController(multiprocessing_context)
        self.assertTrue(controller.start())

    @patch(
        "src.common.config_handler.ConfigHandler.get_frame_provider_config",
        return_value=MagicMock(),
    )
    @patch(
        "src.frameprovider.camera_integration.CameraIntegration.start_camera",
        side_effect=mock_start_camera,
    )
    @patch("src.pcm.controller.ConfigHandler")
    @patch("src.pcm.controller.SocketClient")
    @patch("src.pcm.processor_process.os")
    @patch("src.pcm.provider_process.os")
    def test_controller_start_when_processes_are_running(self, *args):
        """Test to start processes when they are already running."""
        multiprocessing_context = multiprocessing.get_context()
        controller = ProcessController(multiprocessing_context)
        controller.start()
        self.assertFalse(controller.start())

    @patch(
        "src.common.config_handler.ConfigHandler.get_frame_provider_config",
        return_value=MagicMock(),
    )
    @patch(
        "src.frameprovider.camera_integration.CameraIntegration.start_camera",
        side_effect=mock_start_camera,
    )
    @patch("src.pcm.controller.ConfigHandler")
    @patch("src.pcm.controller.SocketClient")
    @patch("src.pcm.processor_process.os")
    @patch("src.pcm.provider_process.os")
    def test_controller_stop_when_processes_are_running(self, *args):
        """Test to stop processes."""
        multiprocessing_context = multiprocessing.get_context()
        controller = ProcessController(multiprocessing_context)
        controller.start()
        self.assertTrue(controller.stop())

    @patch("src.pcm.controller.ConfigHandler")
    @patch("src.pcm.controller.SocketClient")
    @patch("src.pcm.processor_process.os")
    @patch("src.pcm.provider_process.os")
    def test_controller_stop_when_processes_are_not_running(self, *args):
        """Test to stop processes when they are not running."""
        multiprocessing_context = multiprocessing.get_context()
        controller = ProcessController(multiprocessing_context)
        self.assertTrue(controller.stop())

    @patch(
        "src.common.config_handler.ConfigHandler.get_frame_provider_config",
        return_value=MagicMock(),
    )
    @patch(
        "src.frameprovider.camera_integration.CameraIntegration.start_camera",
        side_effect=mock_start_camera,
    )
    @patch("src.pcm.controller.ConfigHandler")
    @patch("src.pcm.controller.SocketClient")
    @patch("src.pcm.processor_process.os")
    @patch("src.pcm.provider_process.os")
    def test_restart_when_processes_are_running(self, *args):
        """Test to restart processes."""
        multiprocessing_context = multiprocessing.get_context()
        controller = ProcessController(multiprocessing_context)
        controller.start()
        self.assertTrue(controller.restart())

    @patch(
        "src.common.config_handler.ConfigHandler.get_frame_provider_config",
        return_value=MagicMock(),
    )
    @patch(
        "src.frameprovider.camera_integration.CameraIntegration.start_camera",
        side_effect=mock_start_camera,
    )
    @patch("src.pcm.controller.ConfigHandler")
    @patch("src.pcm.controller.SocketClient")
    @patch("src.pcm.processor_process.os")
    @patch("src.pcm.provider_process.os")
    def test_restart_when_processes_are_not_running(self, *args):
        """Test to restart processes."""
        multiprocessing_context = multiprocessing.get_context()
        controller = ProcessController(multiprocessing_context)
        self.assertTrue(controller.restart())

    @patch(
        "src.common.config_handler.ConfigHandler.get_frame_provider_config",
        return_value=MagicMock(),
    )
    @patch(
        "src.frameprovider.camera_integration.CameraIntegration.start_camera",
        side_effect=mock_start_camera,
    )
    @patch("src.pcm.controller.ConfigHandler")
    @patch("src.pcm.controller.SocketClient")
    @patch("src.pcm.processor_process.os")
    @patch("src.pcm.provider_process.os")
    def test_restart_when_processes_are_running_and_stop_fails(self, *args):
        """Test to restart processes when stop fails."""
        multiprocessing_context = multiprocessing.get_context()
        controller = ProcessController(multiprocessing_context)
        controller.start()
        controller.stop = lambda: False
        self.assertFalse(controller.restart())

    @patch(
        "src.common.config_handler.ConfigHandler.get_frame_provider_config",
        return_value=MagicMock(),
    )
    @patch(
        "src.frameprovider.camera_integration.CameraIntegration.start_camera",
        side_effect=mock_start_camera,
    )
    @patch("src.pcm.controller.ConfigHandler")
    @patch("src.pcm.controller.SocketClient")
    @patch("src.pcm.processor_process.os")
    @patch("src.pcm.provider_process.os")
    @patch("src.pcm.controller.ProcessController._terminate_process")
    def test_stop_throws_exception_when_process_terminate_fails(
        self, mock_terminate_process, *args
    ):
        """Test to stop processes when terminate fails."""
        multiprocessing_context = multiprocessing.get_context()
        controller = ProcessController(multiprocessing_context)
        controller.start()
        mock_terminate_process.side_effect = Exception("Test Exception")
        with self.assertRaises(Exception):
            controller.stop()

    @patch(
        "src.common.config_handler.ConfigHandler.get_frame_provider_config",
        return_value=MagicMock(),
    )
    @patch(
        "src.frameprovider.camera_integration.CameraIntegration.start_camera",
        side_effect=mock_start_camera,
    )
    @patch("src.pcm.controller.ConfigHandler")
    @patch("src.pcm.controller.SocketClient")
    @patch("src.pcm.processor_process.os")
    @patch("src.pcm.provider_process.os")
    @patch("src.pcm.controller.ProcessQueue")
    def test_stop_calls_queue_clear(self, mock_queue, *args):
        """Test to stop processes."""
        multiprocessing_context = multiprocessing.get_context()
        controller = ProcessController(multiprocessing_context)
        controller.start()
        controller.stop()
        mock_queue.return_value.work_queue.close.assert_called_once()

    @patch("src.pcm.controller.ConfigHandler")
    @patch("src.pcm.processor_process.os")
    @patch("src.pcm.provider_process.os")
    @patch("src.pcm.controller.SocketClient")
    def test_initialize_calls_start_dispatcher(self, mock_socket_client, *args):
        multiprocessing_context = multiprocessing.get_context()
        controller = ProcessController(multiprocessing_context)
        controller.initialize()
        controller.ws.start_dispatcher.assert_called_once()

    @patch("src.pcm.controller.ConfigHandler")
    @patch("src.pcm.processor_process.os")
    @patch("src.pcm.provider_process.os")
    @patch("src.pcm.controller.SocketClient")
    def test_on_message_calls_send_response(self, mock_socket_client, *args):
        multiprocessing_context = multiprocessing.get_context()
        controller = ProcessController(multiprocessing_context)
        controller.on_message('{"type": "request", "command": "start"}')
        self.assertFalse(controller.start())
        mock_socket_client.return_value.send.assert_called_once()
        controller.on_message('{"type": "request", "command": "stop"}')
        self.assertTrue(controller.stop())
        self.assertEquals(mock_socket_client.return_value.send.call_count, 2)
        controller.on_message('{"type": "request", "command": "restart"}')
        self.assertFalse(controller.start())
        self.assertEquals(mock_socket_client.return_value.send.call_count, 3)
        controller.stop()
        controller.on_message('{"type": "request", "command": "invalid"}')
        self.assertTrue(controller.start())
