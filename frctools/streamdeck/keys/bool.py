from .key import StreamDeckKey

import ntcore


def __bool_event__(key):
    def e(event: ntcore.Event):
        key.state = event.data.value.getBoolean()

    return e


def __connection_event__(key):
    inst = ntcore.NetworkTableInstance.getDefault()
    def e(event: ntcore.Event):
        nonlocal inst
        key.state = inst.isConnected()

    return e


class StreamDeckKeyBool(StreamDeckKey):
    def __init__(self, label: str = None, state: bool = False, true_img='white', false_img='black', pressed_callback=None, released_callback=None, held_callback=None):
        super().__init__(pressed_callback, released_callback, held_callback)
        self.__label = label
        self.__state = state

        self.__temp_true_img = true_img
        self.__temp_false_img = false_img

        self.__true_img = None
        self.__false_img = None

        self.__nt_entry = None


    @property
    def label(self):
        return self.__label
    @label.setter
    def label(self, label):
        if self.__label != label:
            self.__label = label

            self.__true_img = None
            self.__false_img = None

            self.update_img()

    @property
    def state(self):
        return self.__state
    @state.setter
    def state(self, state):
        if self.__state != state:
            self.__state = state
            self.update_img()

            if self.__nt_entry is not None:
                self.__nt_entry.setValue(self.__state)

    def bind_nt(self, nt_path: str):
        inst = ntcore.NetworkTableInstance.getDefault()

        self.__nt_entry = inst.getEntry(nt_path)
        inst.addListener(self.__nt_entry, ntcore.EventFlags.kValueAll, __bool_event__(self))

        return self

    def bind_nt_connected(self):
        inst = ntcore.NetworkTableInstance.getDefault()
        inst.addConnectionListener(True, __connection_event__(self))

        return self

    def generate_img(self):
        if self.__true_img is None:
            self.__true_img = self.create_img(self.__temp_true_img, label=self.__label)
            self.__false_img = self.create_img(self.__temp_false_img, label=self.__label)

        if self.__state is True:
            return self.__true_img
        else:
            return self.__false_img