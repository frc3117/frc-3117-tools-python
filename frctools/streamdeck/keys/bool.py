from .key import StreamDeckKey


class StreamDeckKeyBool(StreamDeckKey):
    def __init__(self, label=None, state=False, true_img='white', false_img='black', pressed_callback=None, released_callback=None, held_callback=None):
        super().__init__(pressed_callback, released_callback, held_callback)
        self.__state = state

        self.__temp_true_img = true_img
        self.__temp_false_img = false_img

        self.__true_img = None
        self.__false_img = None


    @property
    def state(self):
        return self.__state
    @state.setter
    def state(self, state):
        if self.__state != state:
            self.__state = state
            self.update_img()

    def bind_nt(self, nt_path: str):
        pass

    def generate_img(self):
        if self.__true_img is None:
            self.__true_img = self.create_img(self.__temp_true_img)
            self.__false_img = self.create_img(self.__temp_false_img)

        if self.__state is True:
            return self.__true_img
        else:
            return self.__false_img