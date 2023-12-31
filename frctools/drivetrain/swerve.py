from frctools import Servo


class SwerveModule:
    def __init__(self, drive_motor, steering_servo: Servo):
        self.drive = drive_motor
        self.steering = steering_servo


class SwerveDrive:
    def __init__(self, modules: list[SwerveModule]):
        self.modules = modules
