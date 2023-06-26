"""This module is used to provide object for sending frames to queue."""

import numpy as np


class LabelExtractionRequest:
    """
    Object for sending frames to queue for frame processor.
    """

    def __init__(self, t_start_frame: float, correlation_id: str, frame: np.ndarray) -> None:
        """
        Initialize the LabelExtractionRequest object.

        @param
            t_start_frame (float): Time of the start of frame capture
            correlation_id (str): Correlation id of the frame
            frame (np.ndarray): Image read from camera
        """
        self.t_start_frame = t_start_frame
        self.frame = frame
        self.correlation_id = correlation_id
