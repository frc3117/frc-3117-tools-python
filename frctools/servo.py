from frctools.frcmath import lerp, repeat
from frctools.timer import Timer, CoroutineOrder

import math


class Servo:
    def __init__(self, motor, encoder, controller, min_max=(-math.pi, math.pi), offset: float = 0.):
        self.__motor = motor
        self.__encoder = encoder
        self.controller = controller

        self.min, self.max = min_max
        self.offset = offset
        self.__target = 0

        self.__coroutine = None

    def start_control(self):
        self.__coroutine = Timer.start_coroutine(self.__control_coroutines__(), CoroutineOrder.LATE)

    def stop_control(self):
        if self.__coroutine is not None:
            Timer.stop_coroutine(self.__coroutine)

    def __control_coroutines__(self):
        while True:
            angle = self.get_angle()
            error = self.__target - angle

            self.__motor.set(self.controller.evaluate(error))
            yield None

    def set(self, target: float):
        self.__target = target

    def get(self):
        return self.__target

    def get_angle(self) -> float:
        encoder = repeat(self.__encoder.get() - self.offset, 1)
        return lerp(self.min, self.max, encoder)
