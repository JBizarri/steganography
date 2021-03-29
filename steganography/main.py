from steganography import Steganography


def main():
    path = "./resources/apyr.jpg"
    s = Steganography(path)

    s.encode("Sample text")
    s.save("./resources/apyr - encoded.jpg")

    print(s.decode("./resources/apyr - encoded.png"))


if __name__ == "__main__":
    main()
