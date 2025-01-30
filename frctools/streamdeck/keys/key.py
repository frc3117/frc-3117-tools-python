try:
    from StreamDeck.ImageHelpers import PILHelper
    from PIL import ImageDraw, ImageFont

    import os

    __DIR__ = os.path.dirname(os.path.realpath(__file__))

    LABEL_FONT = ImageFont.truetype(f'{__DIR__}/Futura.ttc', 12)
    VALUE_FONT = ImageFont.truetype(f'{__DIR__}/Geneva.ttf', 15)

    class StreamDeckKey:
        def __init__(self, pressed_callback=None, released_callback=None, held_callback=None):
            self.pressed_callback = pressed_callback
            self.released_callback = released_callback
            self.held_callback = held_callback

            self.__deck = None
            self.__key = None

            self.__img = None

        def set_key_id(self, deck, key_id):
            self.__deck = deck
            self.__key = key_id

            self.update_img()

        def handle_pressed(self):
            if self.pressed_callback:
                self.pressed_callback()

        def handle_released(self):
            if self.released_callback:
                self.released_callback()

        def handle_held(self):
            if self.held_callback:
                self.held_callback()

        def update(self):
            if self.__deck is not None and self.__img is not None:
                self.__deck.set_key_image(self.__key, self.__img)
                self.__img = None

        def generate_img(self):
            return self.create_img('white')

        def create_img(self, background, label: str = None, value: str = None):
            if isinstance(background, (str, tuple)):
                img = PILHelper.create_key_image(self.__deck, background)
            else:
                img = PILHelper.create_scaled_key_image(self.__deck, background)

            draw = ImageDraw.Draw(img)
            if label is not None:
                draw.text((img.width / 2, (img.height - 15)), text=label, font=LABEL_FONT, anchor='ms', align='center')
            if value is not None:
                draw.text((img.width / 2, (img.height / 2) - 5), text=value, font=VALUE_FONT, anchor='ms', align='center')

            return img

        def update_img(self):
            self.__img = PILHelper.to_native_key_format(self.__deck, self.generate_img())

except ImportError:
    class StreamDeckKey:
        def __init__(self, *args, **kwargs):
            raise RuntimeError("PIL is not installed")
