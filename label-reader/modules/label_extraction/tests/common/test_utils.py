import unittest
from unittest.mock import patch

import numpy as np
from src.common.utils import (
    encode_image,
    is_ascii,
    parse_int_from_str,
    contains_alpha,
    encode_audio,
    convert_to_jpeg,
)


class TestUtils(unittest.TestCase):
    @patch(
        "src.common.utils.cv2.imencode",
        return_value=[None, np.array([1, 2, 3, 4, 5])],
    )
    def test_if_image_is_encoded_correctly(self, *args):
        image = b"test"
        self.assertEqual(
            encode_image(image),
            "data:image/jpeg;base64,AQAAAAAAAAACAAAAAAAAAAMAAAAAAAAABAAAAAAAAAAFAAAAAAAAAA==",
        )

    def test_if_string_is_parsed_correctly(self):
        string = "123"
        self.assertEqual(parse_int_from_str(string), 123)

        string = "123.123"
        self.assertEqual(parse_int_from_str(string), "123.123")

        string = "abc"
        self.assertEqual(parse_int_from_str(string), "abc")

    def test_is_ascii(self):
        self.assertTrue(is_ascii("abc"))
        self.assertFalse(is_ascii("abc\u00e9"))

    def test_contains_alpha(self):
        self.assertTrue(contains_alpha("abc"))
        self.assertTrue(contains_alpha("abc\u00e9"))
        self.assertFalse(contains_alpha("123"))

    def test_encode_audio(self):
        audio = np.array([1, 2, 3, 4, 5])
        self.assertEqual(
            encode_audio(audio),
            "AQAAAAAAAAACAAAAAAAAAAMAAAAAAAAABAAAAAAAAAAFAAAAAAAAAA==",
        )

    def test_convert_to_jpeg(self):
        images = np.array([1, 2, 3, 4, 5])
        self.assertEqual(
            type(convert_to_jpeg(images)),
            bytes,
        )
