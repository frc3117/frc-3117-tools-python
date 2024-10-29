from .key import StreamDeckKey


class StreamDeckKeyBool(StreamDeckKey):
    def __init__(self, label=None, state=False, pressed_callback=None, released_callback=None, held_callback=None):
        super().__init__(pressed_callback, released_callback, held_callback)
        self.state = state

    def set_state(self, state):
        self.state = state

    def on_key_up(self):
        self.set_state(not self.state)
        self.on_key_change(self.state)

    def on_key_change(self, state):
        pass