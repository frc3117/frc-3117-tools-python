from typing import List
from frctools import Component, Coroutine, CoroutineOrder, Timer
from frctools.input import Input
from frctools.frcmath import Vector2, Polar, repeat, lerp, angle_normalize, delta_angle
from enum import Enum

import math
import wpilib
import wpiutil


class SwerveDriveMode(int, Enum):
    FIELD_CENTRIC = 0
    ROBOT_CENTRIC = 1


class SwerveHoldAngle:
    def __init__(self, swerve: 'SwerveDrive', controller):
        self.__swerve = swerve
        self.__controller = controller

        self.__target = 0
        self.__is_running = False

    def set_target(self, target):
        self.__target = target

    def start(self):
        self.__is_running = True

    def stop(self):
        self.__is_running = False

    def is_running(self):
        return self.__is_running

    def __control_loop__(self):
        while True:
            if self.__is_running:
                current = Vector2(0, 1).rotate(self.__swerve.get_heading())
                target = Vector2(0, 1).rotate(self.__target)

                error = current.dot(target)
                self.__swerve.override_axes(horzontal=self.__controller.evaluate(error))
            yield None

    def __iter__(self):
        yield from self.__control_loop__()


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

        self.speed = 1.

        self.rotation_vector = Vector2(position.y, -position.x).normalize()

        self.__translation: Vector2 = Vector2.zero()
        self.__rotation: float = 0.

        self.__target_vec = Vector2.zero()

        self.__last_flip = 1
        self.__last_flip_frame = 0

    def init(self):
        pass

    def update(self, translation: Vector2, rotation: float):
        self.__translation = translation
        self.__rotation = rotation

        self.__compute_vectors__()
        self.__controll_module__()

    def set_axes(self, horizontal: float = None, vertical: float = None, rotation: float = None):
        self.set_horizontal(horizontal)
        self.set_vertical(vertical)
        self.set_rotation(rotation)

    def set_horizontal(self, horizontal: float):
        if horizontal is not None:
            self.__translation.x = horizontal

    def set_vertical(self, vertical: float):
        if vertical is not None:
            self.__translation.y = vertical

    def set_rotation(self, rotation: float):
        if rotation is not None:
            self.__rotation = rotation

    def set_speed(self, speed: float):
        self.speed = speed

    def __compute_vectors__(self):
        # Compute the translation and rotation vectors
        rot = self.rotation_vector * self.__rotation

        # Normalize if the vector is greater than one
        sum_vec = self.__translation + rot
        if sum_vec.magnitude > 1:
            sum_vec.normalize()

        self.__target_vec = sum_vec * self.speed

        self.__translation = Vector2.zero()
        self.__rotation = 0

    def __controll_module__(self):
        if self.__target_vec.magnitude <= 0.01:
            self.drive_motor.set(0)
            self.steering_motor.set(0)

            self.__last_flip = 1
            self.__last_flip_frame = 0

            return

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
        #self.steering_motor.set_voltage(steering)
        self.steering_motor.set(steering)
        self.drive_motor.set(drive)

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


class SwerveDrive(Component):
    def __init__(self, modules: List[SwerveModule],
                 imu: wpilib.ADIS16448_IMU,
                 imu_offset: float = 0.,
                 start_heading: float = 0.):
        super().__init__()

        self.modules = modules
        self.imu = imu

        self.speed = 1.

        self.imu_offset = imu_offset
        self.heading_offset = 0.
        self.set_current_heading(start_heading)

        self.horizontal: Input = Input.get_input('horizontal')
        self.vertical: Input = Input.get_input('vertical')
        self.rotation: Input = Input.get_input('rotation')

        self.drive_mode = SwerveDriveMode.FIELD_CENTRIC

        self.__translation: Vector2 = Vector2()
        self.__rotation: float = 0.

        self.__control_coroutine = None

    def init(self):
        for mod in self.modules:
            mod.init()

    def update(self):
        self.__control_coroutine = Timer.start_coroutine_if_stopped(self.__control_loop__, self.__control_coroutine, CoroutineOrder.LATE)

        self.__translation = Vector2(self.horizontal.get(), self.vertical.get())
        self.__rotation = self.rotation.get()

    def __control_loop__(self):
        while True:
            if self.drive_mode == SwerveDriveMode.FIELD_CENTRIC:
                self.__update_centric__(True)
            elif self.drive_mode == SwerveDriveMode.ROBOT_CENTRIC:
                self.__update_centric__(False)

            yield None

    def override_axes(self, horizontal: float = None, vertical: float = None, rotation: float = None):
        if horizontal is not None:
            self.__translation.x = horizontal
        if vertical is not None:
            self.__translation.y = vertical
        if rotation is not None:
            self.__rotation = rotation

    def __update_centric__(self, use_heading: bool):
        if use_heading:
            self.__translation = self.__translation.rotate(self.get_heading())

        for mod in self.modules:
            mod.update(self.__translation,
                       self.__rotation)

    def set_speed(self, speed: float):
        for mod in self.modules:
            mod.set_speed(speed)

    def set_drive_mode(self, mode:  SwerveDriveMode):
        self.drive_mode = mode

    def get_heading(self):
        return angle_normalize(math.radians(self.imu.getAngle()) - self.imu_offset - self.heading_offset)

    def set_heading_offset(self, offset: float):
        self.heading_offset = offset

    def set_current_heading(self, heading: float):
        self.heading_offset -= delta_angle(self.get_heading(), heading)

    def zero_heading(self):
        self.set_current_heading(0.)

    def initSendable(self, builder: wpiutil.SendableBuilder):
        builder.addDoubleProperty('heading', self.get_heading, lambda v: None)
        for i, mod in enumerate(self.modules):
            curr_mod = mod
            builder.addDoubleProperty(f'{i}/RawSteerAngle', curr_mod.get_stee_rangle_raw, lambda v: None)
            builder.addDoubleProperty(f'{i}/SteerAngle', curr_mod.get_steer_angle, lambda v: None)
            builder.addDoubleProperty(f'{i}/SteerTargetAngle', curr_mod.get_steer_target_angle, lambda v: None)
            builder.addDoubleProperty(f'{i}/DriveSpeed', curr_mod.get_drive_velocity, lambda v: None)
