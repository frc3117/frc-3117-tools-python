from frctools import Timer


class SlewRateLimiter:
    def __init__(self, rate: float):
        self.rate = rate
        self.last_value = 0.0

    def evaluate(self, value: float, dt: float = None) -> float:
        if dt is None:
            dt = Timer.get_delta_time()

        delta = value - self.last_value
        max_delta = self.rate * dt

        if delta > max_delta:
            value = self.last_value + max_delta
        elif delta < -max_delta:
            value = self.last_value - max_delta

        self.last_value = value
        return value

    def __call__(self, value: float, dt: float = None) -> float:
        return self.evaluate(value, dt)
