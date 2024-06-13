from typing import Callable
from frctools import Timer
from frctools.frcmath import clamp

import math
import wpiutil


class PID(wpiutil.Sendable):
    def __init__(self,
                 kp: float,
                 ki: float,
                 kd: float,
                 kf: float = 1.,
                 feed_forward: Callable[[float], float] = None,
                 integral_range=None,
                 reset_integral_on_flip: bool = False):
        super().__init__()
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.kf = kf

        self.__feed_forward = feed_forward

        self.__integral_range = integral_range
        self.__reset_integral_on_flip = reset_integral_on_flip

        self.__previous_error = 0.
        self.__integral = 0.

    def evaluate(self, error: float, feed_forward: float = 0, dt: float = None):
        if dt is None:
            dt = Timer.get_delta_time()

        derivative = (self.__previous_error - error) / dt
        self.__integral += error * dt
        self.__previous_error = error

        if self.__integral_range is not None:
            self.__integral = clamp(self.__integral, self.__integral_range[0], self.__integral_range[1])

        if self.__reset_integral_on_flip and math.copysign(error, self.__previous_error) != error:
            self.__integral = 0

        if self.__feed_forward is not None:
            ff = self.__feed_forward(feed_forward)
        else:
            ff = 0

        return self.kp * error + self.ki * self.__integral + self.kd * derivative + self.kf * ff

    def __get_kp(self):
        return self.kp
    def __set_kp(self, kp):
        self.kp = kp

    def __get_ki(self):
        return self.ki
    def __set_ki(self, ki):
        self.ki = ki

    def __get_kd(self):
        return self.kd
    def __set_kd(self, kd):
        self.kd = kd

    def __get_kf(self):
        return self.kf
    def __set_kf(self, kf):
        self.kf = kf

    def initSendable(self, builder: wpiutil.SendableBuilder, name: str = None):
        prefix = ''
        if name is not None:
            prefix = f'{name}/'

        builder.addDoubleProperty(f'{prefix}Kp', self.__get_kp, self.__set_kp)
        builder.addDoubleProperty(f'{prefix}Ki', self.__get_ki, self.__set_ki)
        builder.addDoubleProperty(f'{prefix}Kd', self.__get_kd, self.__set_kd)

        if self.__feed_forward is not None:
            builder.addDoubleProperty(f'{prefix}Kf', self.__get_kf, self.__set_kf)
