from typing import List
from frctools import Component, Coroutine, CoroutineOrder, Timer
from frctools.input import Input
from frctools.frcmath import Vector2, Polar, repeat, lerp

import math
import wpilib
import wpiutil


class SwerveModule:
    def __init__(self,
                 drive_motor,
                 steering_motor,
                 steering_encoder,
                 steering_controller,
                 steering_offset,
                 position: Vector2):

        self.drive_motor = drive_motor

        self.steering_motor = steering_motor
        self.steering_encoder = steering_encoder
        self.steering_controller = steering_controller
        self.steering_offset = steering_offset

        self.rotation_vector = Vector2(position.y, -position.x).normalized()

        self.__target_vec = Vector2.zero()

        self.__control_coroutine: Coroutine = None

    def init(self):
        pass

    def update(self, translation: Vector2, rotation: float):
        if not self.is_in_control():
            self.__control_coroutine = Timer.start_coroutine(self.__control_loop__(), CoroutineOrder.LATE)

        # Compute the translation and rotation vectors
        rot = self.rotation_vector * rotation

        # Normalize if the vector is greater than one
        sum_vec = translation + rot
        if sum_vec.magnitude() > 1:
            sum_vec = sum_vec.normalized()

        self.__target_vec = sum_vec

    def __control_loop__(self):
        while True:
            if self.__target_vec.magnitude() <= 0.01:
                self.drive_motor.set(0)
                self.steering_motor.set(0)

                yield None
                continue

            # Get the drive motor speed
            drive = self.__target_vec.magnitude()

            # Get the forward vector for the module
            forward = Polar(self.get_steer_angle(), 1)

            # Convert the vector from polar from to cartesian
            forward_vec = forward.to_vector()
            left_vec = forward_vec.rotate(math.pi)

            # Get the normalized target vector
            target_norm = self.__target_vec.normalized()

            # Project the target vector onto the forward and left
            forward_dot = forward_vec.dot(target_norm)
            left_dot = left_vec.dot(target_norm)

            # If the projection on the forward vector is negative. It is faster to flip the drive motor
            if forward_dot < 0:
                drive *= -1
                left_dot *= -1

            # Evaluate the output of the steering pid controller
            steering = self.steering_controller.evaluate(left_dot)

            # Apply the command to the motors
            self.steering_motor.set(steering)
            self.drive_motor.set(drive)

            yield None

    def get_steer_angle(self) -> float:
        encoder = repeat(self.steering_encoder.get() - self.steering_offset, 1)
        return lerp(math.pi, -math.pi, encoder)

    def get_steer_target_angle(self) -> float:
        if self.__target_vec.magnitude() < 0.01:
            return 0

        return math.atan2(self.__target_vec.y, self.__target_vec.x)

    def get_drive_velocity(self) -> float:
        return self.drive_motor.get()

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

    def is_in_control(self) -> bool:
        return self.__control_coroutine is not None and not self.__control_coroutine.is_done


class SwerveDrive(Component):
    def __init__(self, modules: List[SwerveModule], imu: wpilib.ADIS16448_IMU):
        super().__init__()

        self.modules = modules
        self.imu = imu

        self.horizontal: Input = Input.get_input('horizontal')
        self.vertical: Input = Input.get_input('vertical')
        self.rotation: Input = Input.get_input('rotation')

        wpilib.SmartDashboard.putData('SwerveDrive', self)

    def init(self):
        for mod in self.modules:
            mod.init()

    def update(self):
        translation = Vector2(self.horizontal.get(), self.vertical.get()).rotate(self.imu.getAngle())
        rotation = self.rotation.get()

        for mod in self.modules:
            mod.update(translation,
                       rotation)

    def initSendable(self, builder: wpiutil.SendableBuilder) -> None:
        for i, mod in enumerate(self.modules):
            curr_mod = mod
            builder.addDoubleProperty(f'{i}/SteerAngle', curr_mod.get_steer_angle, lambda v: None)
            builder.addDoubleProperty(f'{i}/SteerTargetAngle', curr_mod.get_steer_target_angle, lambda v: None)
            builder.addDoubleProperty(f'{i}/DriveSpeed', curr_mod.get_drive_velocity, lambda v: None)


