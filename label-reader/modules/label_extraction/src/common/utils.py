"""This module is used to provide all utility methods."""
import base64
import re
from typing import Union
import cv2
from numpy import ndarray


def encode_image(image: bytes) -> str:
    """
    Encode image to base64 string.

    @param
        image (bytes): Image data in bytes
    @return
        image_str (str:) Base64 encoded image string
    """
    image = cv2.imencode(".jpg", image)[1].tobytes()
    image = base64.b64encode(image).decode("utf-8")
    image = f"data:image/jpeg;base64,{image}"
    return image


def convert_to_jpeg(images: ndarray) -> bytes:
    """
    Convert images to jpeg.

    @param
        images (numpy.ndarray): Image as Numpy Array
    @return
        jpeg_images (bytes): Images in jpeg format
    """
    jpeg_images = cv2.imencode(".jpg", images)[1]
    return jpeg_images.tobytes()


def parse_int_from_str(string: str) -> Union[int, str]:
    """
    Parse string and convert to int if possible.

    @param
        string (str): String to convert
    @return
        Union[int, str]: Converted int if string is int, otherwise string
    """
    if re.match(r"^([\d]+)$", string):
        return int(string)
    return string


def is_ascii(text: str) -> bool:
    """
    Check if string is ascii.

    @param
        text (str): String to check
    @return
        bool: True if string is ascii, otherwise False
    """
    return all(ord(char) < 128 for char in text)


def contains_alpha(text: str) -> bool:
    """
    Check if string contains alpha characters.

    @param
        text (str): String to check
    @return
        bool: True if string contains alpha characters, otherwise False
    """
    return any(char.isalpha() for char in text)


def encode_audio(audio):
    """
    Encode audio to base64 string.

    @param
        audio (bytes): Audio data in bytes
    @return
        audio_str (str): Base64 encoded audio string
    """
    return base64.b64encode(audio).decode("utf-8")
