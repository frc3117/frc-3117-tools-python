from typing import TypeVar
#from .vector import Vector2

import math
import sys


T = TypeVar('T')

HALF_PI = math.pi / 2
EPSILON = sys.float_info.epsilon


def approximately(a: float, b: float, epsilon=EPSILON) -> bool:
    return abs(a - b) <= epsilon


def clamp(value: float, min_val: float, max_val: float):
    return max(min(value, max_val), min_val)


def deadzone(axis: float, deadzone_val: float) -> float:
    if approximately(axis, 0):
        return 0.
    elif approximately(axis, 1):
        return 1.

    deadzone_axis = clamp((abs(axis) - deadzone_val) / (1 - deadzone_val), 0, 1)
    return math.copysign(deadzone_axis, axis)


def repeat(t: float, length: float) -> float:
    t_abs = abs(t)
    res = clamp(t_abs - math.floor(t_abs / length) * length, 0, length)

    return length - res if t < 0 else res


def angle_normalize(angle: float):
    return repeat(angle, math.tau)


def lerp(a: T, b: T, t: float) -> float:
    return (1 - t) * a + t * b


def inverse_lerp(a: T, b: T, value: T) -> float:
    return (value - a) / (b - a)


def lerp_angle(a: T, b: T, t: float) -> float:
    return angle_normalize((1 - t) * a + t * b)


def delta_angle(current: float, target: float) -> float:
    t = target - current
    length = math.tau

    delta_ang = clamp(t - math.floor(t / length) * length, 0., length)
    return delta_ang - (math.tau if delta_ang > math.pi else 0)

def between(a: float, b: float, v: float, inclusive: bool = True) -> bool:
    if inclusive:
        return a <= v <= b
    return a < v < b


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


def bezier(p0, p1, control, t: float):
    x = (1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * control[0] + t ** 2 * p1[0]
    y = (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * control[1] + t ** 2 * p1[1]

    return x, y
