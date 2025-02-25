from .timer import Timer
from .input import Input
from .component import Component
from .autonomous import AutonomousManager
from .networktables import HarfangsDashboard

from typing import Dict
from enum import Enum

import wpilib


class Alliance(str, Enum):
    RED = 'red'
    BLUE = 'blue'
    UNDEFINED = 'undefined'

    @staticmethod
    def get_alliance() -> 'Alliance':
        alliance = wpilib.DriverStation.getAlliance()
        if alliance is None:
            return Alliance.UNDEFINED

        if alliance == wpilib.DriverStation.Alliance.kRed:
            return Alliance.RED
        if alliance == wpilib.DriverStation.Alliance.kBlue:
            return Alliance.BLUE


class RobotBase(wpilib.TimedRobot):
    __INSTANCE__: 'RobotBase' = None

    def __init__(self):
        super().__init__()

        RobotBase.__INSTANCE__ = self
        self.__components: Dict[str, Component] = {}
        self.__auto_manager = AutonomousManager()
        self.__current_auto: str = None

        self.__auto_selector = wpilib.SendableChooser()
        self.add_auto('none', None)

        self.__loggers = []

        #self.__dashboard__ = HarfangsDashboard.init_roborio()
        wpilib.SmartDashboard.putData('Autonomous', self.__auto_selector)

    def robotInit(self):
        Timer.init()
        Input.init()

    def robotPeriodic(self):
        Timer.evaluate()

    def autonomousInit(self):
        self.__auto_manager.start_auto(self.__auto_selector.getSelected())
        self.__component_init__(lambda comp: comp.init_teleop())

    def autonomousPeriodic(self):
        self.__component_update__(lambda comp: comp.update_auto())

    def autonomousExit(self) -> None:
        self.__auto_manager.end_auto()

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

        for logger in self.__loggers:
            logger.init()

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

    def add_auto(self, name: str, auto, default: bool = False):
        if default:
            self.__auto_selector.setDefaultOption(name, auto)
        else:
            self.__auto_selector.addOption(name, auto)

    def add_logger(self, logger):
        self.__loggers.append(logger)

    def __getitem__(self, index: str) -> Component:
        return self.get_component(index)
    def __setitem__(self, key: str, value: Component):
        self.add_component(key, value)

    @staticmethod
    def instance():
        return RobotBase.__INSTANCE__
