import wpilib


class RobotBase(wpilib.TimedRobot):
    def __init__(self):
        super().__init__()

        self.__components = []

    def robotInit(self):
        pass

    def robotPeriodic(self):
        pass

    def autonomousInit(self):
        for comp in self.__components:
            comp.init()
            comp.init_auto()

    def autonomousPeriodic(self):
        for comp in self.__components:
            comp.update()
            comp.update_auto()

    def teleopInit(self):
        for comp in self.__components:
            comp.init()
            comp.init_teleop()

    def teleopPeriodic(self):
        for comp in self.__components:
            comp.update()
            comp.update_teleop()

    def testInit(self):
        pass

    def testPeriodic(self):
        pass

    def disabledInit(self):
        pass

    def disabledPeriodic(self):
        pass
