from typing import List
from frctools import Component, Servo
from frctools.input import Input
from frctools.frcmath import Vector2, Polar

import math
import wpilib
import wpiutil


class SwerveModule:
    def __init__(self, drive_motor, steering_servo: Servo, position: Vector2):
        self.drive = drive_motor

        self.steering = steering_servo
        self.steering.min = 0
        self.steering.max = math.tau

        self.flipped = False

        self.rotation_vector = Vector2(position.y, -position.x).normalized()

    def init(self):
        pass

    def update(self, horizontal: float, vertical: float, rotation: float):
        if not self.steering.is_in_controll():
            self.steering.start_control()

        # Compute the translation and rotation vectors
        trans = Vector2(horizontal, vertical)
        rot = self.rotation_vector * rotation

        sum_vec = trans + rot

        if sum_vec.magnitude() <= 0.01:
            self.drive.set(0)
            return

        forward = Polar(self.get_steer_angle(), 1)
        if self.flipped:
            forward.rotate(math.pi)
            sum_vec *= -1

        #forward_vec = forward.to_vector()
        #if forward_vec.dot(sum_vec) < 0:
        #    self.flipped = not self.flipped

        sum_polar = Polar.from_vector(sum_vec)
        self.steering.set(sum_polar.theta)
        self.drive.set(sum_polar.radius)
        #self.drive.set(-sum_polar.radius if self.flipped else sum_polar.radius)

    def get_steer_angle(self) -> float:
        return self.steering.get_angle()

    def get_steer_target_angle(self) -> float:
        return self.steering.get()

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

    def is_flipped(self) -> bool:
        return self.flipped


class SwerveDrive(Component):
    def __init__(self, modules: List[SwerveModule]):
        super().__init__()

        self.modules = modules

        self.horizontal: Input = Input.get_input('horizontal')
        self.vertical: Input = Input.get_input('vertical')
        self.rotation: Input = Input.get_input('rotation')

        wpilib.SmartDashboard.putData('SwerveDrive', self)

    def init(self):
        for mod in self.modules:
            mod.init()

    def update(self):
        for mod in self.modules:
            mod.update(self.horizontal.get(),
                       self.vertical.get(),
                       self.rotation.get())

    def initSendable(self, builder: wpiutil.SendableBuilder) -> None:
        for i, mod in enumerate(self.modules):
            curr_mod = mod
            builder.addDoubleProperty(f'{i}/SteerAngle', curr_mod.get_steer_angle, lambda v: None)
            builder.addDoubleProperty(f'{i}/SteerTargetAngle', curr_mod.get_steer_target_angle, lambda v: None)
            builder.addDoubleProperty(f'{i}/DriveSpeed', curr_mod.get_drive_velocity, lambda v: None)
            builder.addBooleanProperty(f'{i}/Flipped', curr_mod.is_flipped, lambda v: None)


