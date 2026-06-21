import os

from PIL import Image, ImageEnhance

WIDTH = 384

def prepare_image(path) -> Image.Image:
     
    img = Image.open(path.lstrip("/")) # TODO: fix hack for windows paths, remove lstrip when fixed

    # 1. convert to grayscale
    img = img.convert("L")

    # 2. optional contrast boost (belangrijk voor thermisch printen)
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(1.4)

    # 3. resize keeping aspect ratio
    ratio = WIDTH / img.width
    new_height = int(img.height * ratio)
    img = img.resize((WIDTH, new_height))

    # 4. Floyd-Steinberg dithering (cruciaal)
    img = img.convert("1")  # default dithering in PIL

    return img