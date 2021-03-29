# Module steganography

## Classes

### Steganography

    Steganography(path: str, end: str = None)

    Steganography class responsible for hiding text inside images
    
    Initialize the class
    
    Args:
        path (str): Path to the image that will hide the text
        end (str, optional): End characters to know when to stop
        decoding. Defaults to "\end".

#### Methods

    decode(self, path: str = None) ‑> str
        Decode image and returns the hidden message
        
        Args:
            path (str, optional): Path of the image, if not specified uses the encoded
            image from self. Defaults to None.
        
        Returns:
            str: Decoded message

    encode(self, message: str) ‑> NoneType
        Encode image with a string message
        
        Args:
            message (str): message to encode

    save(self, path: str) ‑> NoneType
        Save image as png.
        
        Args:
            path (str): path to save image.