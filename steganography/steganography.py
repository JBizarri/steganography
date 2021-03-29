import os
import pathlib
import re

from PIL import Image


class Steganography:
    """Steganography class responsible for hiding text inside images"""

    def __init__(self, path: str, end: str = None) -> None:
        """Initialize the class

        Args:
            path (str): Path to the image that will hide the text
            end (str, optional): End characters to know when to stop
            decoding. Defaults to "\\end".
        """
        self._original_image = Image.open(path)

        self._encoded_image = None
        self._end_message = end or r"\end"

    def encode(self, message: str) -> None:
        """Encode image with a string message

        Args:
            message (str): message to encode
        """
        image = self._original_image.copy()
        width, height = image.size
        pixels = image.load()

        binary_string = self._str_to_binary_string(message + self._end_message)
        tribit_list = self._split(binary_string, 3)

        for x_pixel in range(width):
            for y_pixel in range(height):
                tribit = tribit_list.pop(0)
                rgb_binary = self._rgb_to_binary(pixels[x_pixel, y_pixel])
                new_pixel = self._write_to_lsb(tribit, rgb_binary)

                if len(new_pixel) < 3:
                    new_pixel = self._complete_list(new_pixel, list(rgb_binary))

                pixels[x_pixel, y_pixel] = self._binary_to_rgb(*new_pixel)

                if not tribit_list:
                    break
            else:
                continue
            break

        self._encoded_image = image

    def decode(self, path: str = None) -> str:
        """Decode image and returns the hidden message

        Args:
            path (str, optional): Path of the image, if not specified uses the encoded
            image from self. Defaults to None.

        Returns:
            str: Decoded message
        """
        if path:
            image = Image.open(path)
        else:
            image = self._encoded_image

        width, height = image.size
        pixels = image.load()

        binary_string = ""
        for x_pixel in range(width):
            for y_pixel in range(height):
                rgb = pixels[x_pixel, y_pixel]
                red, blue, green = self._rgb_to_binary(rgb)
                binary_string += red[-1] + blue[-1] + green[-1]

        return self._binary_string_to_str(binary_string, end=self._end_message)

    def save(self, path: str) -> None:
        """Save image as png.

        Args:
            path (str): path to save image.
        """
        path = self._path_as_png(path)

        if self._encoded_image:
            self._encoded_image.save(path)
        else:
            print("Error! Image was not encoded yet.")

    @staticmethod
    def _write_to_lsb(tribit: str, rgb_binary: tuple):
        """Writes tribit to least significant bit from rgb_binary

        Args:
            tribit (str): A string with 3 bits
            rgb_binary (tuple): RGB values as binary

        Returns:
            list: rgb_binary with least significant bits as tribit
        """
        pixel = []
        for idx, bit in enumerate(tribit):
            color = rgb_binary[idx]
            color = color[:-1] + bit
            pixel.append(color)

        return pixel

    @staticmethod
    def _split(string: str, n: int):
        """Split string every n characters.

        Args:
            string (str): String to be splitted.
            n (int): group size.

        Returns:
            list: A list containing substrings of size n.
        """
        return [string[start : start + n] for start in range(0, len(string), n)]

    @staticmethod
    def _complete_list(to_complete: list, from_complete: list):
        """Completes to_complete with values from from_complete

        If to_complete has 1 elements and from_complete as 3, to_complete will
        use the second and third element from from_complete so it also has
        3 elements.

        Args:
            to_complete (list): List with RGB values for a pixel
            from_complete (list): List with RGB values for a pixel

        Returns:
            list: New pixel with the same length as from_complete using the
            latter's values to complete any missing element.
        """
        to_complete_ = list(to_complete).copy()
        from_complete_ = list(from_complete).copy()

        if len(to_complete_) < len(from_complete_):

            n_missing_elements = len(from_complete_) - len(to_complete_)
            start = n_missing_elements * -1
            end = 0
            for i in range(start, end):
                to_complete_.append(from_complete_[i])

        return to_complete_

    @staticmethod
    def _path_as_png(filepath: str):
        """Returns filepath with PNG extension if it's a file.

        Args:
            filepath (str): Path to the file.

        Raises:
            IsADirectoryError: When filepath is a directory.

        Returns:
            str: filepath with png as extension.
        """
        if filepath.strip() == "":
            raise ValueError("filepath can't be an empty string.")
        path = pathlib.Path(filepath)
        suffixes = "".join(path.suffixes)

        if os.path.exists(filepath):
            if os.path.isfile(filepath):
                if suffixes:
                    filepath_without_extension = filepath.rsplit(suffixes, 1)[0]
                else:
                    filepath_without_extension = filepath
            else:
                raise IsADirectoryError(filepath)
        else:
            if filepath.endswith(os.sep):
                raise IsADirectoryError(filepath)

            if suffixes:
                filepath_without_extension = filepath.rsplit(suffixes, 1)[0]
            else:
                print(
                    f"Can't determine if {filepath} is a directory or file."
                    + " Assuming it's a file!"
                )
                filepath_without_extension = filepath

        return filepath_without_extension + ".png"

    @staticmethod
    def _str_to_binary_string(string: str) -> str:
        """Converts regular text to binary.

        Args:
            string (str): Text to be converted.

        Raises:
            ValueError: When return value is empty.

        Returns:
            str: Text as binary.
        """
        binary_string = ""
        for char in string:
            ascii_code = ord(char)
            binary_string += format(ascii_code, "08b")

        if binary_string:
            return binary_string
        else:
            raise ValueError("Error converting message to binary")

    @staticmethod
    def _binary_string_to_str(binary_string: str, end=None) -> str:
        """Converts string with binary numbers to text string

        Args:
            binary_string (str): A string with binary numbers for ASCII
            codes.
            end (string, optional): Stops when end is found. Defaults to None.

        Returns:
            str: Text converted from binary string.
        """
        string = ""

        binary_list = re.findall("." * 8, binary_string)
        for byte in binary_list:
            string += chr(int(byte, 2))
            if end and string.endswith(end):
                return string[: -len(end)]

        return string

    @staticmethod
    def _rgb_to_binary(rgb: tuple) -> tuple:
        """Converts tuple of decimal string to binary

        Args:
            rgb (tuple): An RGB tuple. Example: (255, 255, 255).

        Raises:
            ValueError: When the tuple is not of length 3.

        Returns:
            tuple: Binary tuple.
            Example ("11111111", "11111111", "11111111").
        """
        if len(rgb) != 3:
            raise ValueError("RGB must be a tuple with 3 values")

        red, green, blue = tuple(map(int, rgb))

        r_binary = format(red, "08b")
        g_binary = format(green, "08b")
        b_binary = format(blue, "08b")

        return (r_binary, g_binary, b_binary)

    @staticmethod
    def _binary_to_rgb(*args) -> tuple:
        """Converts RGB binary values to decimal.

        Returns:
            tuple: RGB values in the decimal system.
        """
        if len(args) == 1:
            red = args[0][0]
            green = args[0][1]
            blue = args[0][2]
        elif len(args) == 3:
            red = args[0]
            green = args[1]
            blue = args[2]
        else:
            raise ValueError(
                "Arguments must be RGB tuple or Red, Green, Blue as 3 arguments."
            )

        r_int = int(red, 2)
        g_int = int(green, 2)
        b_int = int(blue, 2)

        return (r_int, g_int, b_int)
