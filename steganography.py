import re

from PIL import Image


class Steganography:
    def __init__(self, path: str) -> None:
        self._original_image = Image.open(path)

        self._encoded_image = None

    def encode(self, message: str) -> None:
        image = self._original_image.copy()
        width, height = image.size
        pixels = image.load()

        binary_string = self._str_to_binary_string(message)
        tribit_list = re.findall("...", binary_string)

        for x_pixel in range(width):
            for y_pixel in range(height):
                tribit = tribit_list.pop(0)
                rgb = pixels[x_pixel, y_pixel]
                red, green, blue = self._rgb_to_binary(rgb)

                red = red[:-1] + tribit[0]
                green = green[:-1] + tribit[1]
                blue = blue[:-1] + tribit[2]

                rgb = self._binary_to_rgb(red, green, blue)
                pixels[x_pixel, y_pixel] = rgb

                if not tribit_list:
                    break
            else:
                continue
            break

        self._encoded_image = image

    def decode(self, path: str = None) -> str:
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

        return self._binary_string_to_str(binary_string)

    def save(self, path: str, original_image: bool = False) -> None:
        if not original_image and self._encoded_image is not None:
            self._encoded_image.save(path)
        elif not original_image and self._encoded_image is None:
            print("Error! Image was not encoded yet.")
        else:
            self._original_image.save(path)

    @staticmethod
    def _str_to_binary_string(string: str) -> str:
        binary_string = ""
        for char in string:
            ascii_code = ord(char)
            binary_string += format(ascii_code, "08b")

        if binary_string:
            return binary_string
        else:
            raise ValueError("Error converting message to binary")

    @staticmethod
    def _binary_string_to_str(binary_string: str) -> str:
        string = ""

        binary_list = re.findall("." * 8, binary_string)
        for byte in binary_list:
            string += chr(int(byte, 2))

        return string

    @staticmethod
    def _rgb_to_binary(rgb: tuple) -> tuple:
        if len(rgb) != 3:
            raise ValueError("RGB must be a tuple with 3 values")

        red, green, blue = tuple(map(int, rgb))

        r_binary = format(red, "08b")
        g_binary = format(green, "08b")
        b_binary = format(blue, "08b")

        return (r_binary, g_binary, b_binary)

    @staticmethod
    def _binary_to_rgb(*args) -> tuple:
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
