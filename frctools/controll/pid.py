from frctools import Timer
from frctools.frcmath import clamp

import wpiutil


class PID(wpiutil.Sendable):
    def __init__(self, kp: float, ki: float, kd: float):
        super().__init__()
        self.kp = kp
        self.ki = ki
        self.kd = kd

        self.__previous_error = 0.
        self.__integral = 0.

    def evaluate(self, error: float, dt: float = None):
        if dt is None:
            dt = Timer.get_delta_time()

        derivative = (self.__previous_error - error) / dt
        self.__integral += error * dt
        self.__previous_error = error

        self.__integral = clamp(self.__integral, -1, 1)

        return self.kp * error + self.ki * self.__integral + self.kd * derivative

    def initSendable(self, builder: wpiutil.SendableBuilder, name: str = None):
        def set_kp(kp):
            self.kp = kp

        def set_ki(ki):
            self.ki = ki

        def set_kd(kd):
            self.kd = kd

        prefix = ''
        if name is not None:
            prefix = f'{name}/'

        builder.addDoubleProperty(f'{prefix}Kp', lambda: self.kp, lambda v: set_kp(v))
        builder.addDoubleProperty(f'{prefix}Ki', lambda: self.ki, lambda v: set_ki(v))
        builder.addDoubleProperty(f'{prefix}Kd', lambda: self.kd, lambda v: set_kd(v))
