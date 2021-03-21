from steganography import Steganography


def main():
    path = "/mnt/c/Users/Jefferson/Pictures/apyr.jpg"
    s = Steganography(path)
    
    s.encode("Teste")
    s.save("/mnt/c/Users/Jefferson/Pictures/apyr 2.jpg")
    
    with open("/mnt/c/Users/Jefferson/Pictures/decoded_message.txt", "w") as file:
        file.write(s.decode())


if __name__ == "__main__":
    main()
