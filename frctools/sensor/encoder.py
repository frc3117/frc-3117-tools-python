from frctools.frcmath import repeat


class Encoder:
    def __init__(self, encoder, offset, reversed: bool = False):
        self.__encoder = encoder
        self.__offset = offset
        self.__reversed = reversed

    def get(self):
        val = self.__encoder.get() - self.__offset
        if self.__reversed:
            val = 1 - val

        return repeat(val, 1)

    def get_raw(self):
        return self.__encoder.get()
