import wpilib

from frctools.drivetrain import SwerveDrive, SwerveModule
from frctools.frcmath import Vector2


class RobotBase(wpilib.TimedRobot):
    def __init__(self):
        super().__init__()

        self.swerve = None

    def robotInit(self):
        vec = Vector2(1, 1)
        vec += (1, 2)

        print(vec)

        self.swerve = SwerveDrive([
            SwerveModule(wpilib.PWMSparkMax(0), None),
            SwerveModule(wpilib.PWMSparkMax(1), None),
            SwerveModule(wpilib.PWMSparkMax(2), None),
            SwerveModule(wpilib.PWMSparkMax(3), None)
        ])

    def robotPeriodic(self):
        pass

    def autonomousInit(self):
        pass

    def autonomousPeriodic(self):
        pass

    def teleopInit(self):
        pass

    def teleopPeriodic(self):
        pass

    def testInit(self):
        pass

    def testPeriodic(self):
        pass

    def disabledInit(self):
        pass

    def disabledPeriodic(self):
        pass


if __name__ == '__main__':
    wpilib.run(RobotBase)