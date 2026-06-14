from escpos.printer import Network
from PIL import Image, ImageEnhance

PRINTER_IP = "192.168.1.99"
PRINTER_PORT = 9100

IMAGE_PATH = "paard.png"  # zet je foto hier

WIDTH = 384  # safe thermal width for TM-T88IV

def prepare_image(path):
    img = Image.open(path)

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


def main():
    p = Network(PRINTER_IP, port=PRINTER_PORT)

    # init printer (belangrijk op Epson ESC/POS)
    p.text("\x1b@")

    # title
    p.set(align="center", bold=True)
    p.text("=== TEST PRINT ===\n")
    p.set(bold=False)
    p.text("----------------------\n\n")

    # image
    img = prepare_image(IMAGE_PATH)
    p.image(img)

    # spacing + cut
    p.cut()


if __name__ == "__main__":
    main()