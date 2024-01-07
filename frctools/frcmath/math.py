import math

TAU = math.pi * 2


def clamp(value, min_val, max_val):
    return max(min(value, max_val), min_val)


def deadzone(axis, deadzone_val):
    deadzone_axis = clamp((abs(axis) - deadzone_val) / (1 - axis), 0, 1)
    return math.copysign(deadzone_axis, axis)
