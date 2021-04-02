import os
import string
from unittest.mock import MagicMock

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


def test_save_successful(test_image, tmp_folder):
    # ARRANGE
    s = Steganography(test_image)
    s.encode("doesnt matter")

    mock_png_path = os.path.join(tmp_folder, "save_sucess.png")
    s._path_as_png = MagicMock(return_value=mock_png_path)

    # ACT
    s.save(mock_png_path)

    # ASSERT
    assert os.path.exists(mock_png_path)


def test_save_not_successful(test_image, tmp_folder):
    # ARRANGE
    s = Steganography(test_image)

    mock_png_path = os.path.join(tmp_folder, "save_not_sucessful.png")
    s._path_as_png = MagicMock()

    # ACT
    s.save(mock_png_path)

    # ASSERT
    assert not os.path.exists(mock_png_path)
    s._path_as_png.assert_not_called()


def test_write_to_lsb(test_image):
    # ARRANGE
    mocked_tribit = "110"
    mocked_rgb_binary = ("10000000", "10000000", "10000000")

    expected_result = ["10000001", "10000001", "10000000"]

    # ACT
    result = Steganography(test_image)._write_to_lsb(mocked_tribit, mocked_rgb_binary)

    # ASSERT
    assert result == expected_result


def test_split_every_3_characters_with_12_characters(test_image):
    # ARRANGE
    mocked_string_to_split = "000111222333444"
    expected_result = ["000", "111", "222", "333", "444"]

    # ACT
    result = Steganography(test_image)._split(mocked_string_to_split, 3)

    # ASSERT
    assert result == expected_result


def test_split_every_3_characters_with_8_characters(test_image):
    # ARRANGE
    mocked_string_to_split = "12345678"
    expected_result = ["123", "456", "78"]

    # ACT
    result = Steganography(test_image)._split(mocked_string_to_split, 3)

    # ASSERT
    assert result == expected_result


def test_split_every_3_characters_with_7_characters(test_image):
    # ARRANGE
    mocked_string_to_split = "1234567"
    expected_result = ["123", "456", "7"]

    # ACT
    result = Steganography(test_image)._split(mocked_string_to_split, 3)

    # ASSERT
    assert result == expected_result


def test_complete_list_missing_1_element(test_image):
    # ARRANGE
    to_complete = [1, 2]
    from_complete = [4, 5, 6]

    expected_result = [1, 2, 6]

    # ACT
    result = Steganography(test_image)._complete_list(to_complete, from_complete)

    # ASSERT
    assert result == expected_result


def test_complete_list_missing_2_elements(test_image):
    # ARRANGE
    to_complete = [1]
    from_complete = [4, 5, 6]

    expected_result = [1, 5, 6]

    # ACT
    result = Steganography(test_image)._complete_list(to_complete, from_complete)

    # ASSERT
    assert result == expected_result


def test_complete_list_missing_all_elements(test_image):
    # ARRANGE
    to_complete = []
    from_complete = [4, 5, 6]

    expected_result = [4, 5, 6]

    # ACT
    result = Steganography(test_image)._complete_list(to_complete, from_complete)

    # ASSERT
    assert result == expected_result


def test_complete_list_no_missing_elements(test_image):
    # ARRANGE
    to_complete = [1, 2, 3]
    from_complete = [4, 5, 6]

    expected_result = [1, 2, 3]

    # ACT
    result = Steganography(test_image)._complete_list(to_complete, from_complete)

    # ASSERT
    assert result == expected_result


def test_complete_list_to_complete_gt_from_complete(test_image):
    # ARRANGE
    to_complete = [1, 2, 3, 4]
    from_complete = [4, 5, 6]

    expected_result = [1, 2, 3, 4]

    # ACT
    result = Steganography(test_image)._complete_list(to_complete, from_complete)

    # ASSERT
    assert result == expected_result


def test_path_as_png_if_jpg_file(test_image, tmp_folder):
    # ARRANGE
    mocked_filepath = os.path.join(tmp_folder, "some_jpg_file.jpg")
    with open(mocked_filepath, "w") as f:
        f.write("")

    expected_result = os.path.join(tmp_folder, "some_jpg_file.png")

    # ACT
    result = Steganography(test_image)._path_as_png(mocked_filepath)

    # ASSERT
    assert result == expected_result


def test_path_as_png_if_two_extensions(test_image, tmp_folder):
    # ARRANGE
    mocked_filepath = os.path.join(tmp_folder, "some_targz_file.tar.gz")
    with open(mocked_filepath, "w") as f:
        f.write("")

    expected_result = os.path.join(tmp_folder, "some_targz_file.png")

    # ACT
    result = Steganography(test_image)._path_as_png(mocked_filepath)

    # ASSERT
    assert result == expected_result


def test_path_as_png_if_empty_path(test_image):
    # ARRANGE
    mocked_filepath = ""

    # ACT / ASSERT
    with pytest.raises(ValueError):
        Steganography(test_image)._path_as_png(mocked_filepath)


def test_path_as_png_if_file_exists_but_no_extension(test_image, tmp_folder):
    # ARRANGE
    mocked_filepath = os.path.join(tmp_folder, "some_file_without_extension")
    with open(mocked_filepath, "w") as f:
        f.write("")

    expected_result = os.path.join(tmp_folder, "some_file_without_extension.png")

    # ACT
    result = Steganography(test_image)._path_as_png(mocked_filepath)

    # ASSERT
    assert result == expected_result


def test_path_as_png_if_directory_exists(test_image, tmp_folder):
    # ARRANGE / ACT / ASSERT
    with pytest.raises(IsADirectoryError):
        Steganography(test_image)._path_as_png(tmp_folder)


def test_path_as_png_when_path_does_not_exist_and_is_directory(test_image):
    # ARRANGE
    mocked_filepath = "/some/path/"

    # ACT / ASSERT
    with pytest.raises(IsADirectoryError):
        Steganography(test_image)._path_as_png(mocked_filepath)


def test_path_as_png_when_path_does_not_exist_and_could_be_file_or_directory(
    test_image, capfd
):
    # ARRANGE
    mocked_filepath = "/some/path"
    expected_result = "/some/path.png"

    # ACT
    result = Steganography(test_image)._path_as_png(mocked_filepath)
    output, _ = capfd.readouterr()

    # ASSERT
    assert result == expected_result
    assert "Assuming it's a file" in output


def test_str_to_binary_string_if_no_text_passed(test_image):
    # ARRANGE
    mocked_string = ""

    # ACT / ASSERT
    with pytest.raises(ValueError):
        Steganography(test_image)._str_to_binary_string(mocked_string)


def test_str_to_binary_string(test_image):
    # ARRANGE
    mocked_string = "This is a test string that is being tested in this test."
    expected_result = (
        "01010100011010000110100101110011001000000110100101110011001000000110000100100"
        + "000011101000110010101110011011101000010000001110011011101000111001001101001"
        + "011011100110011100100000011101000110100001100001011101000010000001101001011"
        + "100110010000001100010011001010110100101101110011001110010000001110100011001"
        + "010111001101110100011001010110010000100000011010010110111000100000011101000"
        + "11010000110100101110011001000000111010001100101011100110111010000101110"
    )

    # ACT
    result = Steganography(test_image)._str_to_binary_string(mocked_string)

    # ASSERT
    assert result == expected_result


def test_binary_string_to_str(test_image):
    # ARRANGE
    mocked_binary_string = (
        "01010100011010000110100101110011001000000110100101110011001000000110000100100"
        + "000011101000110010101110011011101000010000001110011011101000111001001101001"
        + "011011100110011100100000011101000110100001100001011101000010000001101001011"
        + "100110010000001100010011001010110100101101110011001110010000001110100011001"
        + "010111001101110100011001010110010000100000011010010110111000100000011101000"
        + "11010000110100101110011001000000111010001100101011100110111010000101110"
    )
    expected_result = "This is a test string that is being tested in this test."

    # ACT
    result = Steganography(test_image)._binary_string_to_str(mocked_binary_string)

    # ASSERT
    assert result == expected_result


def test_binary_string_to_str_if_end_character(test_image):
    # ARRANGE
    # This is a test string that is being tested in this test.\end
    mocked_binary_string = (
        "01010100011010000110100101110011001000000110100101110011001000000110000100100"
        + "000011101000110010101110011011101000010000001110011011101000111001001101001"
        + "011011100110011100100000011101000110100001100001011101000010000001101001011"
        + "100110010000001100010011001010110100101101110011001110010000001110100011001"
        + "010111001101110100011001010110010000100000011010010110111000100000011101000"
        + "110100001101001011100110010000001110100011001010111001101110100001011100101"
        + "1100011001010110111001100100"
    )
    expected_result = "This is a test string that is being tested in this test."

    # ACT
    result = Steganography(test_image)._binary_string_to_str(
        mocked_binary_string, r"\end"
    )

    # ASSERT
    assert result == expected_result


def test_binary_string_to_str_if_end_character_and_text_after(test_image):
    # ARRANGE
    # This is a test string.\endNOW SOME CHARACTERS THAT SHOULD NOT BE SEEN
    mocked_binary_string = (
        "01010100011010000110100101110011001000000110100101110011001000000110000100100"
        + "000011101000110010101110011011101000010000001110011011101000111001001101001"
        + "011011100110011100101110010111000110010101101110011001000100111001001111010"
        + "101110010000001010011010011110100110101000101001000000100001101001000010000"
        + "010101001001000001010000110101010001000101010100100101001100100000010101000"
        + "100100001000001010101000010000001010011010010000100111101010101010011000100"
        + "010000100000010011100100111101010100001000000100001001000101001000000101001"
        + "1010001010100010101001110"
    )
    expected_result = "This is a test string."

    # ACT
    result = Steganography(test_image)._binary_string_to_str(
        mocked_binary_string, r"\end"
    )

    # ASSERT
    assert result == expected_result


def test_rgb_to_binary(test_image):
    # ARRANGE
    mocked_rgb = (123, 1, 32)
    expected_result = ("01111011", "00000001", "00100000")

    # ACT
    result = Steganography(test_image)._rgb_to_binary(mocked_rgb)

    # ASSERT
    assert result == expected_result


def test_rgb_to_binary_if_invalid_rgb_length(test_image):
    # ARRANGE
    mocked_rgb = (123, 1)

    # ACT / ASSERT
    with pytest.raises(ValueError):
        Steganography(test_image)._rgb_to_binary(mocked_rgb)


def test_binary_to_rgb(test_image):
    # ARRANGE
    mocked_binary_rgb = ("01111011", "00000001", "00100000")
    expected_result = (123, 1, 32)

    # ACT
    result = Steganography(test_image)._binary_to_rgb(mocked_binary_rgb)

    # ASSERT
    assert result == expected_result


def test_binary_to_rgb_if_unpacking(test_image):
    # ARRANGE
    mocked_binary_rgb = ["01111011", "00000001", "00100000"]
    expected_result = (123, 1, 32)

    # ACT
    result = Steganography(test_image)._binary_to_rgb(*mocked_binary_rgb)

    # ASSERT
    assert result == expected_result


def test_binary_to_rgb_if_invalid_arguments(test_image):
    # ARRANGE
    mocked_binary_rgb = ["01111011", "00000001"]

    # ACT / ASSERT
    with pytest.raises(ValueError):
        Steganography(test_image)._binary_to_rgb(*mocked_binary_rgb)
