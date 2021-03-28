# Steganography

A simple steganography algorithm. This is project is really simple (and not inovative at all 😅) and is being developed for fun on my free time only, as of consequence is not intented to be complex or extensive.

"Steganography is the practice of concealing a message within another message or a physical object. In computing/electronic contexts, a computer file, message, image, or video is concealed within another file, message, image, or video. " - Wikipedia

This code will take any text and put it inside a image.

>Disclaimer: it is NOT recommended using this if you intend to actually hide text inside an image as it's not really hard to decode the message.

## Run working example

Create a virtual environment

`python3 -m virtualenv venv`

Install requirements

`pip3 install -r requirements.txt`

Run

`python3 main.py`

You should see `Sample text` printed on your console.

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
