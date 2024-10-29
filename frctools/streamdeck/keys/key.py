try:
    from StreamDeck.ImageHelpers import PILHelper


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

            self.__img = self.generate_img()

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
            img = PILHelper.create_key_image(deck=self.__deck, background='white')
            return PILHelper.to_native_key_format(self.__deck, img)
except ImportError:
    class StreamDeckKey:
        def __init__(self, *args, **kwargs):
            raise RuntimeError("PIL is not installed")
