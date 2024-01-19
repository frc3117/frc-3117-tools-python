from .timer import Timer
from .component import Component

from typing import Dict

import wpilib


class RobotBase(wpilib.TimedRobot):
    def __init__(self):
        super().__init__()

        self.__components: Dict[str, Component] = {}

    def robotInit(self):
        pass

    def robotPeriodic(self):
        if self.isEnabled():
            Timer.evaluate()

    def autonomousInit(self):
        for name, comp in self.__components.items():
            comp.init()
            comp.init_auto()

    def autonomousPeriodic(self):
        Timer.evaluate()

        for name, comp in self.__components.items():
            comp.update()
            comp.update_auto()

    def teleopInit(self):
        for name, comp in self.__components.items():
            comp.init()
            comp.init_teleop()

    def teleopPeriodic(self):
        Timer.evaluate()
        for name, comp in self.__components.items():
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

    def disabledExit(self):
        Timer.init()

    def add_component(self, name: str, component: Component):
        self.__components[name] = component

