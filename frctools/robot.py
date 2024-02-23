from .timer import Timer
from .input import Input
from .component import Component

from typing import Dict

import wpilib


class RobotBase(wpilib.TimedRobot):
    __INSTANCE__: 'RobotBase' = None

    def __init__(self):
        super().__init__()

        RobotBase.__INSTANCE__ = self
        self.__components: Dict[str, Component] = {}

    def robotInit(self):
        Timer.init()
        Input.init()

    def robotPeriodic(self):
        Timer.evaluate()

    def autonomousInit(self):
        self.__component_init__(lambda comp: comp.init_teleop)

    def autonomousPeriodic(self):
        self.__component_update__(lambda comp: comp.update_auto)

    def teleopInit(self):
        self.__component_init__(lambda comp: comp.init_teleop())

    def teleopPeriodic(self):
        self.__component_update__(lambda comp: comp.update_teleop())

    def testInit(self):
        pass

    def testPeriodic(self):
        pass

    def disabledInit(self):
        pass

    def disabledPeriodic(self):
        pass

    def disabledExit(self):
        Timer.reset()

    def add_component(self, name: str, component: Component):
        self.__components[name] = component
        wpilib.SmartDashboard.putData(name, component)

    def get_component(self, name: str):
        return self.__components[name]

    def __component_init__(self, action):
        for name, comp in self.__components.items():
            comp.init()
            if action is not None:
                action(comp)

    def __component_update__(self, action):
        Timer.do_early_coroutines()

        for name, comp in self.__components.items():
            try:
                comp.update()
                if action is not None:
                    action(comp)
            except Exception as e:
                print(e)

        Timer.do_coroutines()
        Timer.do_late_coroutines()

    @staticmethod
    def instance():
        return RobotBase.__INSTANCE__
