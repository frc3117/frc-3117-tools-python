from frctools.frcmath.math import approximately
from .key import StreamDeckKey

import ntcore


def __double_event__(key):
    def e(event: ntcore.Event):
        key.value = event.data.value.getDouble()

    return e


class StreamDeckKeyDouble(StreamDeckKey):
    def __init__(self, label: str = None, value: float = 0., background='white', pressed_callback=None, released_callback=None, held_callback=None):
        super().__init__(pressed_callback, released_callback, held_callback)
        self.__label = label
        self.__value = value

        self.__background = background

        self.__nt_entry = None

    @property
    def label(self):
        return self.__label
    @label.setter
    def label(self, label):
        if self.__label != label:
            self.__label = label

            self.update_img()

    @property
    def value(self):
        return self.__value
    @value.setter
    def value(self, value):
        if not approximately(self.__value, value):
            self.__value = value
            self.update_img()

            if self.__nt_entry is not None:
                self.__nt_entry.setValue(self.__value)

    def bind_nt(self, nt_path: str):
        inst = ntcore.NetworkTableInstance.getDefault()

        self.__nt_entry = inst.getEntry(nt_path)
        inst.addListener(self.__nt_entry, ntcore.EventFlags.kValueAll, __double_event__(self))

        return self

    def generate_img(self):
        return self.create_img(self.__background, self.label, str(round(self.value, 3)))