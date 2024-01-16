import math

HALF_PI = math.pi / 2


def clamp(value: float, min_val: float, max_val: float):
    return max(min(value, max_val), min_val)


def deadzone(axis: float, deadzone_val: float) -> float:
    deadzone_axis = clamp((abs(axis) - deadzone_val) / (1 - axis), 0, 1)
    return math.copysign(deadzone_axis, axis)


def repeat(t: float, length: float) -> float:
    return clamp(t - math.floor(t / length) * length, 0, length)


def delta_angle(current: float, target: float) -> float:
    delta = repeat((target - current), math.tau)
    if delta > HALF_PI:
        return delta - math.pi

    return delta


def __get_power_of__(num: float, power: float, method) -> float:
    if num <= 0:
        return 1

    return math.pow(power, method(math.log(num, power)))


def get_closest_power_of(num: float, power) -> float:
    return __get_power_of__(num, power, round)


def get_next_power_of(num: float, power: float) -> float:
    return __get_power_of__(num, power, math.ceil)


def get_previous_power_of(num: float, power: float) -> float:
    return __get_power_of__(num, power, math.floor)
