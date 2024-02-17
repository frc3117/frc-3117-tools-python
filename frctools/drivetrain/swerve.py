from typing import List
from frctools import Component, Coroutine, CoroutineOrder, Timer
from frctools.input import Input
from frctools.frcmath import Vector2, Polar, repeat, lerp, angle_normalize

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

        self.rotation_vector = Vector2(position.y, -position.x).normalize()

        self.__target_vec = Vector2.zero()

        self.__last_flip = 1
        self.__last_flip_frame = 0

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
        if sum_vec.magnitude > 1:
            sum_vec.normalize()

        self.__target_vec = sum_vec

    def __control_loop__(self):
        while True:
            if self.__target_vec.magnitude <= 0.01:
                self.drive_motor.set(0)
                self.steering_motor.set(0)

                self.__last_flip = 1
                self.__last_flip_frame = 0

                yield None
                continue

            # Get the drive motor speed
            drive = self.__target_vec.magnitude

            # Get the forward vector for the module
            forward = Polar(self.get_steer_angle(), 1)

            # Convert the vector from polar from to cartesian
            forward_vec = forward.to_vector()
            left_vec = forward_vec.rotate(math.pi / 2)

            # Get the normalized target vector
            target_norm = self.__target_vec.normalized()

            target_norm *= self.__last_flip
            drive *= self.__last_flip

            # Project the target vector onto the forward and left
            forward_dot = forward_vec.dot(target_norm)
            left_dot = left_vec.dot(target_norm)

            curr_frame = Timer.get_frame_count()

            # If the projection on the forward vector is negative. It is faster to flip the drive motor
            if forward_dot < 0 and (curr_frame - self.__last_flip_frame >= 5):
                drive *= -1
                left_dot *= -1

                self.__last_flip *= -1
                self.__last_flip_frame = curr_frame

            # Evaluate the output of the steering pid controller
            steering = self.steering_controller.evaluate(left_dot)

            # Apply the command to the motors
            self.steering_motor.set(steering)
            self.drive_motor.set(drive)

            yield None

    def get_stee_rangle_raw(self):
        return self.steering_encoder.get()

    def get_steer_angle(self) -> float:
        encoder = repeat(self.steering_encoder.get() - self.steering_offset, 1)
        return lerp(math.pi, -math.pi, encoder)

    def get_steer_target_angle(self) -> float:
        if self.__target_vec.magnitude < 0.01:
            return 0

        return math.atan2(self.__target_vec.y, self.__target_vec.x)

    def get_drive_velocity(self) -> float:
        return self.drive_motor.get()

    def get_instant_vector_raw(self) -> Vector2:
        angle = self.get_steer_angle()
        vel = self.get_drive_velocity()

        return Vector2(vel * math.cos(angle),
                       vel * math.sin(angle))

    def is_in_control(self) -> bool:
        return self.__control_coroutine is not None and not self.__control_coroutine.is_done


class SwerveDrive(Component):
    def __init__(self, modules: List[SwerveModule],
                 imu: wpilib.ADIS16448_IMU,
                 imu_offset: float = 0.,
                 start_heading: float = 0.):
        super().__init__()

        self.modules = modules
        self.imu = imu

        self.imu_offset = imu_offset
        self.heading_offset = 0.
        self.set_current_heading(start_heading)

        self.horizontal: Input = Input.get_input('horizontal')
        self.vertical: Input = Input.get_input('vertical')
        self.rotation: Input = Input.get_input('rotation')

    def init(self):
        for mod in self.modules:
            mod.init()

    def update(self):
        translation = Vector2(self.horizontal.get(), self.vertical.get()).rotate(self.get_heading())
        rotation = self.rotation.get()

        for mod in self.modules:
            mod.update(translation,
                       rotation)

    def get_heading(self):
        return angle_normalize(math.radians(self.imu.getAngle()) - self.imu_offset - self.heading_offset)

    def set_heading_offset(self, offset: float):
        self.heading_offset = offset

    def set_current_heading(self, heading: float):
        self.heading_offset = angle_normalize(math.radians(self.imu.getAngle() - self.imu_offset) - heading)

    def zero_heading(self):
        self.set_current_heading(0.)

    def initSendable(self, builder: wpiutil.SendableBuilder):
        for i, mod in enumerate(self.modules):
            curr_mod = mod
            builder.addDoubleProperty(f'{i}/RawSteerAngle', curr_mod.get_stee_rangle_raw, lambda v: None)
            builder.addDoubleProperty(f'{i}/SteerAngle', curr_mod.get_steer_angle, lambda v: None)
            builder.addDoubleProperty(f'{i}/SteerTargetAngle', curr_mod.get_steer_target_angle, lambda v: None)
            builder.addDoubleProperty(f'{i}/DriveSpeed', curr_mod.get_drive_velocity, lambda v: None)
