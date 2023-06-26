"""This module is used to preform camera integration."""
import time
import uuid
import cv2
import numpy as np
from websocket import ABNF
import msgpack

from rx import Observable, operators as op, interval
from src.common.socket_client import SocketClient
from src.common.utils import convert_to_jpeg
from src.frameprovider.label_extraction_request import LabelExtractionRequest
from src.pcm.queue import ProcessQueue
from src.common.log_helper import get_logger
from src.common.config_handler import ConfigHandler


class Frame:
    def __init__(
        self,
        frame: np.ndarray,
        t_start_frame: float,
        correlation_id: str,
        frame_jpg=None,
    ) -> None:
        self.frame = frame
        self.t_start_frame = t_start_frame
        self.correlation_id = correlation_id
        self.frame_jpg = frame_jpg


class CameraIntegration:
    """
    Intergrate with camera, read frames and emit frame to the WebAppAPI and Queue, controlled by FPS
    """

    def __init__(self, queue: ProcessQueue) -> None:
        """
        Initialize the camera integration.

        @param
            queue (ProcessQueue): Queue to add frames to
        """
        self.queue = queue
        config_handler = ConfigHandler()
        self.config = config_handler.get_frame_provider_config()
        self.logger = get_logger(
            component_name=CameraIntegration.__name__,
        )
        self.ws = None
        self.vid = None

    def _get_camera(self, camera_path: str) -> cv2.VideoCapture:
        """
        Get camera.

        @param
            camera_path (str): Path to camera
        @return
            camera_object (cv2.VideoCapture): cv2 camera object
        """
        try:
            vid = cv2.VideoCapture(camera_path)
            return vid
        except Exception as ex:
            self.logger.exception(ex)
            self.logger.error(f"Error opening video stream {ex}")
            raise ex

    def _get_frame_stream(self, frame_rate: float) -> Observable:
        """
        Get frame stream.

        @param
            frame_rate (float): Frame rate for ui
        @return
            frame_stream (Observable): Frame stream object
        """
        frame_stream = interval(frame_rate).pipe(
            op.map(lambda _: self.vid.read()),  # read frame
            op.do_action(
                lambda result: self.vid.set(cv2.CAP_PROP_POS_FRAMES, 0)
                if result[0] is False
                else None
            ),  # restart video on completion
            op.filter(
                lambda result: result[0] is True and result[1] is not None
            ),  # filter None frames
            op.map(lambda result: result[1]),  # get frame
            op.map(
                lambda frame: Frame(
                    frame=frame,
                    t_start_frame=time.time(),
                    correlation_id=str(uuid.uuid4()),
                )
            ),  # create frame object
            op.share(),  # share frame stream
        )
        return frame_stream

    def _emit_frame_to_queue(
        self, frame_stream: Observable, queue_fps: float, frame_size: list
    ) -> Observable:
        """
        Emit frame to queue.

        @param
            frame_stream (Observable): Frame stream object
            queue_fps (float): Frame rate for queue
            frame_size (list): Frame size for queue (width, height)
        @return
            frame_stream (Observable): Frame stream object
        """
        return frame_stream.pipe(
            op.sample(queue_fps),
            op.map(
                lambda frame: Frame(
                    cv2.resize(frame.frame, frame_size),
                    frame.t_start_frame,
                    frame.correlation_id,
                )
            ),
            op.map(lambda frame: self._write_to_queue(frame=frame)),
        )

    def _write_to_queue(self, frame: Frame) -> bool:
        """
        Write frame to queue.

        @param
            frame (bytes): Frame to send to queue
        @return
            result (bool): Result of writing frame to queue, True for success
        """
        try:
            label_extraction_request = LabelExtractionRequest(
                t_start_frame=frame.t_start_frame,
                correlation_id=frame.correlation_id,
                frame=frame.frame,
            )
            return self.queue.add_item(label_extraction_request)
        except Exception as ex:
            self.logger.exception(ex)
            self.logger.error(f"Error reading video stream {ex}")
            return False

    def _connect_to_socket(self) -> None:
        """
        Connect to socket.
        """
        self.ws = SocketClient(
            self.config.vid_stream_socket_url
        )  # TODO: read all config from env variables
        self.ws.connect()
        self.ws.start_dispatcher()

    def _emit_frame_to_socket(
        self, frame_stream: Observable, socket_fps: float, frame_size: list
    ) -> Observable:
        """
        Emit frame to socket.

        @param
            frame_stream (Observable): Frame stream object
            frame_size (list): Frame size for socket (width, height)
        @return
            frame_stream (Observable): Frame stream object
        """
        return frame_stream.pipe(
            op.sample(socket_fps),
            op.map(
                lambda frame: Frame(
                    cv2.resize(frame.frame, frame_size),
                    frame.t_start_frame,
                    frame.correlation_id,
                )
            ),
            op.map(
                lambda frame: Frame(
                    frame.frame,
                    frame.t_start_frame,
                    frame.correlation_id,
                    convert_to_jpeg(frame.frame),
                )
            ),
            op.map(lambda frame: self._write_to_socket(frame=frame)),
        )

    def _write_to_socket(self, frame: Frame) -> bool:
        """
        Write frame to socket.

        @param
            frame (str): Frame to send to socket
        @return
            result (bool): Result of writing frame to socket, True for success
        """
        try:
            return self.ws.send(
                msgpack.dumps(
                    {
                        "raw_frame": frame.frame_jpg,
                        "correlation_id": frame.correlation_id,
                    }
                ),
                ABNF.OPCODE_BINARY,
            )
        except Exception as ex:
            self.logger.exception(ex)
            self.logger.error(f"Error writting video stream to socket {ex}")
            return False

    def start_camera(self) -> None:
        """
        Start camera in infinite loop.
        """
        self._connect_to_socket()
        self.vid = self._get_camera(self.config.camera_path)
        self.logger.info("Started camera...")

        frame_stream = self._get_frame_stream(1 / self.config.frame_rate_camera)

        socket_result_stream = self._emit_frame_to_socket(
            frame_stream, 1 / self.config.frame_rate_ui, self.config.frame_size_ui
        )
        queue_result_stream = self._emit_frame_to_queue(
            frame_stream, 1 / self.config.frame_rate_queue, self.config.frame_size_queue
        )
        socket_result_stream.subscribe(
            on_next=lambda _: None,
            on_error=lambda ex: self.logger.exception(ex),
            on_completed=lambda: self.logger.info("Completed frame stream"),
        )
        queue_result_stream.subscribe(
            on_next=lambda _: None,
            on_error=lambda ex: self.logger.exception(ex),
            on_completed=lambda: self.logger.info("Completed frame stream"),
        )
        self.logger.info("Started camera stream...")
        while True:
            if not self.vid.isOpened():
                self.logger.error("Could not open video device, reconnecting to camera")
                self.vid = self._get_camera(self.config.camera_path)

            time.sleep(10)
