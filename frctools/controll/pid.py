from frctools import Timer


class PID:
    def __init__(self, kp: float, ki: float, kd: float):
        self.kp = kp
        self.ki = ki
        self.kd = kd

        self.__previous_error = 0.
        self.__integral = 0.

    def evaluate(self, error: float, dt: float = None):
        if dt is None:
            dt = Timer.get_delta_time()

        derivative = (self.__previous_error - error) / dt
        self.__integral = error * dt
        self.__previous_error = error

        return self.kp * error + self.ki * self.__integral + self.kd * derivative