

from PIL import Image


class DummyPrinter:
    def text(self, text):
        print(text, end="")

    def cut(self):
        print("--- CUT ---")

    def set(self, **kwargs):
        pass

    def image(self, image: Image.Image):
        print(f"--- IMAGE {image.size} ---")