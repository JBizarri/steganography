# Steganography

A simple steganography algorithm.

"Steganography is the practice of concealing a message within another message or a physical object. In computing/electronic contexts, a computer file, message, image, or video is concealed within another file, message, image, or video. " - Wikipedia

This code will take any text and put it inside a image.

## Run working example

Create a virtual environment

`python3 -m virtualenv venv`

Install requirements

`pip3 install -r requirements.txt`

Run

`python3 main.py`

Open `resources/decoded_message.txt`. You should see `Sample text` as the first words.


## How it works

1. Convert each letter from the secret message to ASCII code, the word "Dog" for example:

    - D: 68

    - o: 111

    - g: 103

2. Convert each ASCII code to binary, following the last example:

    - 68: &nbsp;01000100

    - 111: 01101111

    - 103: 01100111

3. Change the least significative bit for every pixel in the image to the bits from your message.

![Steganography Process](./docs/resources/steganography.png)
