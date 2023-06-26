"""This module is used to provide the text detection request object."""
import numpy as np


class TextDetectionRequest:
    """
    TextDetectionRequest class.
    """

    def __init__(self, image: np.ndarray) -> None:
        """
        Initialize the TextDetectionRequest class.

        @param
            image (np.ndarray): image
        """
        self.image = image
