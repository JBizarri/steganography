import os

import pytest

from steganography.steganography import Steganography


@pytest.fixture
def test_image():
    return "./resources/apyr.jpg"


def test_encode_and_decode(tmp_folder, test_image):
    # ARRANGE
    s = Steganography(test_image)

    text = "Here's the text that should be hidden in the image"

    # ACT
    s.encode(text)

    tmp_file = os.path.join(tmp_folder, "image.jpg")
    s.save(tmp_file)

    result = s.decode(tmp_file.replace("jpg", "png"))

    # ASSERT

    assert result.startswith(text)
