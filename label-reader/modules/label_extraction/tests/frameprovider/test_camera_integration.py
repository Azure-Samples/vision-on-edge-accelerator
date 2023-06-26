import unittest
from unittest.mock import MagicMock, patch
from rx import operators as ops
from rx.testing.marbles import marbles_testing, ReactiveTest, TestScheduler

from src.frameprovider.camera_integration import CameraIntegration, Frame

on_next = ReactiveTest.on_next


def print_marbles(stream, ts):
    diagram = stream.pipe(ops.to_marbles(timespan=ts)).run()
    print('got        "{}"'.format(diagram))


class TestCameraIntegration(unittest.TestCase):
    @patch("src.frameprovider.camera_integration.ConfigHandler")
    @patch(
        "src.frameprovider.camera_integration.cv2.resize", side_effect=lambda x, _: x
    )
    @patch(
        "src.frameprovider.camera_integration.CameraIntegration._write_to_queue",
        side_effect=lambda frame: True,
    )
    def test__emit_frame_to_queue_samples_at_given_rate(self, _, *args):
        frame_rate = 1.0 / 2.0
        ci = CameraIntegration(None)
        ts = 1.0 / 10.0
        mock_frame = Frame(None, None, None)
        with marbles_testing(timespan=ts) as (start, cold, hot, exp):
            # e1 = cold("-a--------b------c----|")
            e1 = cold(
                "-a-b-c---d-e-----|",
                {
                    "a": mock_frame,
                    "b": mock_frame,
                    "c": mock_frame,
                    "d": mock_frame,
                    "e": mock_frame,
                },
            )
            ex = exp(
                " -----c----d----e----|",
                {
                    "c": True,
                    "d": True,
                    "e": True,
                },
            )
            expected = ex

            result_stream = ci._emit_frame_to_queue(e1, frame_rate, [900, 900])
            print_marbles(result_stream, ts)

            results = start(result_stream)
            assert results == expected

    @patch("src.frameprovider.camera_integration.ConfigHandler")
    @patch(
        "src.frameprovider.camera_integration.cv2.resize", side_effect=lambda x, _: x
    )
    @patch(
        "src.frameprovider.camera_integration.convert_to_jpeg",
        side_effect=lambda x: x,
    )
    @patch(
        "src.frameprovider.camera_integration.CameraIntegration._write_to_socket",
        side_effect=lambda frame: True,
    )
    def test__emit_frame_to_socket_samples_at_given_rate(self, _, *args):
        frame_rate = 1.0 / 2.0
        ci = CameraIntegration(None)
        ts = 1.0 / 10.0
        mock_frame = Frame(None, None, None)
        with marbles_testing(timespan=ts) as (start, cold, hot, exp):
            # e1 = cold("-a--------b------c----|")
            e1 = cold(
                "-a-b-c---d-e-----|",
                {
                    "a": mock_frame,
                    "b": mock_frame,
                    "c": mock_frame,
                    "d": mock_frame,
                    "e": mock_frame,
                },
            )
            ex = exp(
                " -----c----d----e----|",
                {
                    "c": True,
                    "d": True,
                    "e": True,
                },
            )
            expected = ex

            result_stream = ci._emit_frame_to_socket(e1, frame_rate, [900, 900])
            print_marbles(result_stream, ts)

            results = start(result_stream)
            assert results == expected

    @patch("src.frameprovider.camera_integration.ConfigHandler")
    @patch(
        "src.frameprovider.camera_integration.cv2.resize",
        side_effect=lambda frame, _: frame,
    )
    @patch(
        "src.frameprovider.camera_integration.convert_to_jpeg",
        side_effect=lambda frame: frame,
    )
    @patch(
        "src.frameprovider.camera_integration.CameraIntegration._write_to_socket",
        side_effect=lambda frame: True if frame.correlation_id == "s" else False,
    )
    def test_emit_frame_to_socket_emits_True_if_write_to_socket_is_success(self, *args):
        ci = CameraIntegration(None)
        ts = 1.0
        success_frame = Frame(None, None, "s")
        failure_frame = Frame(None, None, "f")
        with marbles_testing(timespan=ts) as (start, cold, hot, exp):
            # e1 = cold("-a--------b------c----|")
            e1 = cold(
                "-a-b-c---|",
                {"a": success_frame, "b": failure_frame, "c": success_frame},
            )
            ex = exp(" -a-b-c---|", {"a": True, "b": False, "c": True})
            expected = ex

            result_stream = ci._emit_frame_to_socket(e1, ts, [900, 900])
            print_marbles(result_stream, ts)

            results = start(result_stream)
            assert results == expected

    @patch("src.frameprovider.camera_integration.ConfigHandler")
    def test_write_to_queue_returns_false_in_case_of_exception(self, *args):
        queue = MagicMock()
        queue.add_item.side_effect = Exception("test")
        ci = CameraIntegration(queue)
        result = ci._write_to_queue(None)
        assert result is False

    @patch("src.frameprovider.camera_integration.ConfigHandler")
    def test_write_to_socket_returns_false_in_case_of_exception(self, *args):
        ci = CameraIntegration(None)
        result = ci._write_to_socket(None)
        assert result is False

    @patch(
        "src.frameprovider.camera_integration.cv2.VideoCapture",
        side_effect=Exception("test"),
    )
    @patch("src.frameprovider.camera_integration.ConfigHandler")
    def test__get_camera_raises_exception_if_VideoCapture_throws_exception(self, *args):
        ci = CameraIntegration(None)
        with self.assertRaises(Exception):
            ci._get_camera("")

    @patch("src.frameprovider.camera_integration.ConfigHandler")
    @patch("src.frameprovider.camera_integration.CameraIntegration._connect_to_socket")
    @patch("src.frameprovider.camera_integration.CameraIntegration._get_frame_stream")
    @patch(
        "src.frameprovider.camera_integration.CameraIntegration._emit_frame_to_socket"
    )
    @patch(
        "src.frameprovider.camera_integration.CameraIntegration._emit_frame_to_queue"
    )
    @patch("time.sleep", side_effect=InterruptedError("test"))
    def test_start_camera_restarting_if_camera_in_not_opened(self, *args):
        ci = CameraIntegration(None)
        with patch.object(ci, "_get_camera") as mock_get_camera:
            first_camera_call = MagicMock()
            first_camera_call.isOpened.return_value = False
            second_camera_call = MagicMock()
            second_camera_call.isOpened.return_value = True
            mock_get_camera.side_effect = [first_camera_call, second_camera_call]
            try:
                ci.start_camera()
            except InterruptedError:
                self.assertTrue(ci.vid == second_camera_call)

    @patch("src.frameprovider.camera_integration.ConfigHandler")
    def test__get_frame_stream_filters_invalid_frames(self, *args):
        cam_frame = MagicMock()
        frame = Frame(cam_frame, 0, "")
        with patch("src.frameprovider.camera_integration.Frame", return_value=frame):
            ci = CameraIntegration(None)
            ci.vid = MagicMock()
            ci.vid.read.side_effect = [
                (True, None),
                (True, cam_frame),
                (False, None),
                (True, cam_frame),
            ]
            scheduler = TestScheduler()
            result = scheduler.start(lambda: ci._get_frame_stream(100), disposed=700.0)
            assert result.messages == [
                on_next(400.0, frame),
                on_next(600.0, frame),
            ]
