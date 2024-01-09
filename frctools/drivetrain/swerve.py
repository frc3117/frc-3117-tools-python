from typing import List
from frctools import Servo
from frctools.input import Input
from frctools.frcmath import Vector2, Polar, TAU

import math


class SwerveModule:
    def __init__(self, drive_motor, steering_servo: Servo, position: Vector2):
        self.drive = drive_motor
        self.steering = steering_servo

        self.flipped = False

        self.rotation_vector = Vector2(position.y, -position.x)

    def get_steer_angle(self) -> float:
        return self.steering.get_angle()

    def get_drive_velocity(self) -> float:
        return self.drive.get()

    def get_instant_vector_raw(self) -> Vector2:
        angle = self.get_steer_angle()
        vel = self.get_drive_velocity()

        return Vector2(vel * math.cos(angle),
                       vel * math.sin(angle))

    def get_instant_vector(self) -> Vector2:
        raw = self.get_instant_vector_raw()
        if self.flipped:
            return raw * -1

        return raw

    def start(self):
        pass

    def update(self, horizontal: float, vertical: float, rotation: float):
        # Compute the translation and rotation vectors
        trans = Vector2(horizontal, vertical)
        rot = self.rotation_vector * rotation

        sum_vec = trans + rot

        # Should we do a flip?
        instant = self.get_instant_vector()
        if sum_vec.dot(instant) < 0:
            self.flipped = not self.flipped
            instant *= -1


class SwerveDrive:
    def __init__(self, modules: List[SwerveModule]):
        self.modules = modules

        self.horizontal: Input = Input.get_input('horizontal')
        self.vertical: Input = Input.get_input('vertical')
        self.rotation: Input = Input.get_input('rotation')

    def start(self):
        for mod in self.modules:
            mod.start()

    def update(self):
        for mod in self.modules:
            mod.update(self.horizontal.get(),
                       self.vertical.get(),
                       self.rotation.get())
