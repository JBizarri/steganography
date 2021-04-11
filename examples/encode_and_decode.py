import os

from steganography import Steganography


def main():
    path = "examples/apyr.jpg"
    path = os.path.abspath(path)
    s = Steganography(path)

    s.encode("Sample text")
    s.save("examples/apyr - encoded.jpg")

    print(s.decode("examples/apyr - encoded.png"))


if __name__ == "__main__":
    main()
