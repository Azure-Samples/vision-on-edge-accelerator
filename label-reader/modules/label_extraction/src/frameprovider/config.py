"""This module is used to provide config object for FrameProvider."""
from typing import List, Union


class FrameProviderConfig:
    """
    Configuration for the frame provider
    """

    def __init__(
        self,
        frame_rate_ui: int,
        frame_size_ui: List,
        frame_size_queue: List,
        camera_path: Union[str, int],
        vid_stream_internal_url: str,
        frame_rate_camera: int,
    ) -> None:
        """
        Initialize the config object.

        @param:
        frame_rate_ui (int): FPS rate for UI
        frame_size_ui (List): Frame size as (width, height)
        frame_size_queue (List): Frame size as (width, height)
        camera_path (str|int): Path to the camera
        vid_stream_internal_url (str): Internal URL of the video stream
        frame_rate_camera (int): FPS rate of the camera
        """
        self.frame_rate_ui = frame_rate_ui
        self.frame_size_ui = frame_size_ui
        self.frame_size_queue = frame_size_queue
        self.camera_path = camera_path
        self.frame_rate_queue = 5
        self.vid_stream_socket_url = vid_stream_internal_url
        self.frame_rate_camera = frame_rate_camera
