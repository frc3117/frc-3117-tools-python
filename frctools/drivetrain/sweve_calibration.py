from frctools import Component, Timer, CoroutineOrder
from frctools.input import Input
from typing import List

import math


def smallest_angle(x: float, y: float) -> float:
    a = (x - y) % math.tau
    b = (y - x) % math.tau

    if a < b:
        return -a
    return b


class SwerveCalibratorModule:
    def __init__(self, drive_motor, direction_motor, direction_encoder):
        self.__drive_motor = drive_motor
        self.__direction_motor = direction_motor
        self.__direction_encoder = direction_encoder

        self.__direction_offset = 0.
        self.__direction_encoder_inverted = False
        self.__direction_motor_inverted = False

        self.__drive_encoder_inverted = False
        self.__drive_motor_inverted = False

    def set_direction(self, speed: float):
        self.__direction_motor.set(speed)

    def set_drive(self, speed: float):
        self.__drive_motor.set(speed)

    def zero_direction(self):
        self.__direction_offset = self.get_raw_direction()

    def set_direction_encoder_inverted(self, state: bool):
        self.__direction_encoder_inverted = state

    def set_direction_motor_inverted(self, state: bool):
        self.__direction_motor.set_inverted(state)
        self.__direction_motor_inverted = state

    def set_drive_encoder_inverted(self, state: bool):
        self.__drive_encoder_inverted = state

    def set_drive_motor_inverted(self, state: bool):
        self.__drive_motor.set_inverted(state)
        self.__drive_motor_inverted = state

    def get_raw_direction(self) -> float:
        return self.__direction_encoder.get()

    def get_raw_direction_angle(self) -> float:
        return self.get_raw_direction() * 2. * math.pi

    def get_direction(self) -> float:
        raw = self.get_raw_direction()

        if raw >= self.__direction_offset:
            direction = raw - self.__direction_offset
        else:
            direction = raw + self.__direction_offset

        if self.__direction_encoder_inverted:
            return 1 - direction

        return direction

    def get_direction_angle(self) -> float:
        return self.get_direction() * 2 * math.pi

    def get_drive_velocity(self) -> float:
        velocity = self.__drive_motor.get()
        return velocity * -1 if self.__drive_encoder_inverted else -1

    def reset(self):
        self.set_direction_encoder_inverted(False)
        self.set_direction_motor_inverted(False)

        self.set_drive_encoder_inverted(False)
        self.set_drive_motor_inverted(False)

        self.__direction_offset = 0.

    def print_calibration(self, name: str):
        print(
            f'------------ {name} -----------\n',
            f'Direction Offset: {self.__direction_offset:.4f}\n',
            f'Direction Encoder Inverted: {self.__direction_encoder_inverted}\n',
            f'Direction Motor Inverted: {self.__direction_motor_inverted}\n' 
            '\n',
            f'Drive Encoder Inverted: {self.__drive_encoder_inverted}\n',
            f'Drive Motor Inverted: {self.__drive_motor_inverted}'
        )


class SwerveCalibrator(Component):
    def __init__(self, modules: List[SwerveCalibratorModule]):
        super().__init__()
        self.__modules = modules

        self.__next_button_input = Input.get_input('next_button')
        self.__drive_axis = Input.get_input('drive')
        self.__dir_axis = Input.get_input('direction')

        for mod in self.__modules:
            mod.reset()

    def start(self):
        Timer.start_coroutine(self.__sequence__())

    def next_button(self) -> bool:
        return self.__next_button_input.get_button_up()

    def wait_for_next(self):
        yield None
        while not self.next_button():
            yield None

    def __sequence__(self):
        yield None

        # Align Direction
        yield from self.__align_direction__()

        # Turn Direction
        yield from self.__turn_direction__()

        # Turn Drive
        yield from self.__turn_drive__()

        # Motor Auto
        yield from self.__motor_auto__()

        for i, mod in enumerate(self.__modules):
            mod.print_calibration(f'Swerve {i}')

        yield from self.__test_drive__()

    def __align_direction__(self):
        print('Align all the swerve module in position to move forward')
        yield from self.wait_for_next()

        for mod in self.__modules:
            mod.zero_direction()

    def __turn_direction__(self):
        prev_direction_angle = []
        direction_distance = [0.] * len(self.__modules)

        for i, mod in enumerate(self.__modules):
            prev_direction_angle.append(mod.get_direction_angle())

        print('Rotate each swerve module 45 degree clockwise.')

        yield None
        while not self.next_button():
            for i, mod in enumerate(self.__modules):
                curr_angle = mod.get_direction_angle()

                direction_distance[i] += smallest_angle(prev_direction_angle[i], curr_angle)
                prev_direction_angle[i] = curr_angle

            yield None

        for i, mod in enumerate(self.__modules):
            mod.set_direction_encoder_inverted(direction_distance[i] < 0)

    def __turn_drive__(self):
        drive_distance = [0.] * len(self.__modules)

        print('Rotate each wheel 1 full rotation in the direction which would make the robot move forward.')

        yield None
        while not self.next_button():
            for i, mod in enumerate(self.__modules):
                drive_distance[i] += mod.get_drive_velocity() * 0.02

            yield None

        for i, mod in enumerate(self.__modules):
            mod.set_drive_encoder_inverted(drive_distance[i] < 0)

    def __motor_auto__(self):
        prev_direction_angle = []
        direction_distance = [0.] * len(self.__modules)
        drive_distance = [0.] * len(self.__modules)

        for i, mod in enumerate(self.__modules):
            prev_direction_angle.append(mod.get_direction_angle())

        print('Let the robot rotate the motors for a few seconds.')

        yield None
        while not self.next_button():
            for i, mod in enumerate(self.__modules):
                mod.set_direction(0.2)
                mod.set_drive(0.2)

                curr_angle = mod.get_direction_angle()

                direction_distance[i] += smallest_angle(prev_direction_angle[i], curr_angle)
                prev_direction_angle[i] = curr_angle

                drive_distance[i] += mod.get_drive_velocity() * 0.02

            yield None

        for i, mod in enumerate(self.__modules):
            mod.set_direction_motor_inverted(direction_distance[i] < 0)
            mod.set_drive_motor_inverted(drive_distance[i] < 0)

    def __test_drive__(self):
        yield None
        while True:
            drive_axis = self.__drive_axis.get()
            dir_axis = self.__dir_axis.get()

            for mod in self.__modules:
                mod.set_drive(drive_axis)
                mod.set_direction(dir_axis)

            yield None
