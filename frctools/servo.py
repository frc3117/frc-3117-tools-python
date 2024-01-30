from frctools.frcmath import lerp, repeat, delta_angle
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

    def is_in_controll(self):
        if self.__coroutine is None:
            return False

        return not self.__coroutine.is_done

    def __control_coroutines__(self):
        while True:
            try:
                angle = self.get_angle()
                error = delta_angle(angle, self.__target)

                controll = self.controller.evaluate(error)
                self.__motor.set(controll)
            except Exception as e:
                print(e)
            finally:
                yield None

    def set(self, target: float):
        self.__target = target

    def get(self):
        return self.__target

    def get_angle(self) -> float:
        encoder = repeat(self.__encoder.get() - self.offset, 1)
        return lerp(self.min, self.max, encoder)
