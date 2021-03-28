import pathlib
import re

from PIL import Image


class Steganography:
    def __init__(self, path: str, end: str = None) -> None:
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
                    new_pixel = self._complete_new_pixel(new_pixel, rgb_binary)

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
            path (str, optional): Path of the image, if not specified uses the encoded image from self. Defaults to None.

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
    def _complete_new_pixel(new_pixel: list, old_pixel: tuple):
        """Completes new_pixel with values from old_pixel

        If new_pixel has 1 elements and old_pixel as 3, new_pixel will
        use the second and third element from old_pixel so it also has
        3 elements.

        Args:
            new_pixel (list): List with RGB values for a pixel
            old_pixel (tuple): List with RGB values for a pixel

        Returns:
            list: New pixel with the same length as old_pixel using the
            latter's values to complete any missing element.
        """
        if len(new_pixel) < len(old_pixel):
            new_pixel_ = list(new_pixel).copy()

            n_missing_elements = len(old_pixel) - len(new_pixel_)
            start = -1
            end = (n_missing_elements + 1) * -1
            for i in range(start, end, -1):
                new_pixel_.append(old_pixel[i])

        return new_pixel_

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
        path = pathlib.Path(filepath)
        if path.is_dir():
            raise IsADirectoryError(path)

        suffixes = "".join(path.suffixes)
        filename = filepath.rsplit(suffixes, 1)[0]

        return filename + ".png"

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
            ValueError(
                "Arguments must be RGB tuple or Red, Green, Blue as 3 arguments."
            )

        r_int = int(red, 2)
        g_int = int(green, 2)
        b_int = int(blue, 2)

        return (r_int, g_int, b_int)
