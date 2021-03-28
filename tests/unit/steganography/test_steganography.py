import os
import string

import pytest

from steganography.steganography import Steganography


@pytest.fixture
def test_image():
    return "./resources/apyr.jpg"


@pytest.fixture
def random_words(random):
    def random_word():
        letters = string.ascii_lowercase
        length = random.randint(10, 80)
        return "".join(random.choice(letters) for _ in range(length))

    return [random_word() for _ in range(10)]


def test_encode_and_decode_with_path_for_decoding(tmp_folder, test_image, random_words):
    # ARRANGE
    for idx, word in enumerate(random_words):
        s = Steganography(test_image)

        # ACT
        s.encode(word)

        tmp_file = os.path.join(tmp_folder, f"image{idx}.jpg")
        s.save(tmp_file)

        result = s.decode(tmp_file.replace("jpg", "png"))

        # ASSERT
        assert result == word


def test_encode_and_decode_without_path_for_decoding(test_image, random_words):
    # ARRANGE
    for word in random_words:
        s = Steganography(test_image)

        # ACT
        s.encode(word)
        result = s.decode()

        # ASSERT
        assert result == word
