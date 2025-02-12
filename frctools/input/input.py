from typing import Dict, Union
from enum import Enum

import wpilib
import wpiutil
from wpilib import Joystick

from frctools import frcmath, Timer, CoroutineOrder


class XboxControllerInput(str, Enum):
    A = 'button.1'
    B = 'button.2'
    X = 'button.3'
    Y = 'button.4'
    LB = 'button.5'
    RB = 'button.6'
    BACK = 'button.7'
    START = 'button.8'
    LEFT_JOYSTICK_BUTTON = 'button.9'
    RIGHT_JOYSTICK_BUTTON = 'button.10'

    LEFT_JOYSTICK_X = 'axis.0'
    LEFT_JOYSTICK_Y = 'axis.1'
    LEFT_TRIGGER = 'axis.2'
    RIGHT_TRIGGER = 'axis.3'
    RIGHT_JOYSTICK_X = 'axis.4'
    RIGHT_JOYSTICK_Y = 'axis.5'


class PowerTransform:
    def __init__(self, power: float):
        self.power = max(power, 0)

    def evaluate(self, value: float) -> float:
        return abs(value) ** self.power * (1. if value >= 0 else -1.)

    def __call__(self, value: float) -> float:
        return self.evaluate(value)


class Input(wpiutil.Sendable):
    BUTTON_MODE = 0
    AXIS_MODE = 1
    COMPOSITE_AXIS_MODE = 2

    __joysticks__: Dict[int, Joystick] = {}
    __inputs__: Dict[str, 'Input'] = {}

    def __init__(self, name: str,
                 joystick_id: int = -1,
                 input_id: str = None,
                 inverted: bool = False,
                 deadzone: float = 0.1,
                 mode: int = 1,
                 positive: 'Input' = None,
                 negative: 'Input' = None,
                 axis_filter=None,
                 axis_transform=None):
        super().__init__()
        self.name = name
        self.joystick_id = joystick_id
        self.mode = mode

        if None in [positive, negative]:
            # If the joystick hasn't been initialized yet, initialize it.
            if joystick_id not in Input.__joysticks__:
                Input.__joysticks__[joystick_id] = Joystick(joystick_id)

            # Input IDs are formatted either as
            #   '{mode}.{id}' ex:('button.1' or 'axis.1') or
            #   '{id}' ex:('1', '2') it then use the mode to determine if the irl input is a button or axis.
            split = input_id.split('.')
            if len(split) == 1:
                self.input_id = int(split[0])
                self.__irl_mode__ = mode
            elif len(split) == 2:
                if split[0] == 'button':
                    self.input_id = int(split[1])
                    self.__irl_mode__ = Input.BUTTON_MODE
                elif split[0] == 'axis':
                    self.input_id = int(split[1])
                    self.__irl_mode__ = Input.AXIS_MODE
            else:
                raise ValueError(f'Invalid input ID "{input_id}".')
        else:
            self.positive = positive
            self.negative = negative

        self.deadzone = deadzone
        self.invert = inverted

        self.cutoff = 0.5
        self.click_value = 1.0

        self.__filter = axis_filter
        self.__transform = axis_transform

        if self.mode == Input.AXIS_MODE or self.mode == Input.COMPOSITE_AXIS_MODE:
            self.__last_value = 0.
            self.__current_value = 0.
        elif self.mode == Input.BUTTON_MODE:
            self.__last_value = False
            self.__current_value = False

        wpilib.SmartDashboard.putData(f'inputs/{name}', self)

    def get(self) -> Union[bool, float]:
        if self.mode == Input.BUTTON_MODE:
            return self.__current_value

        return self.__evaluate_axis__(self.__current_value)

    def get_raw(self) -> Union[bool, float]:
        return self.__current_value

    def get_button_up(self) -> bool:
        return self.__last_value and not self.__current_value

    def get_button_down(self) -> bool:
        return not self.__last_value and self.__current_value

    def set_inverted(self, inverted: bool) -> 'Input':
        self.invert = inverted
        return self

    def set_deadzone(self, deadzone: float) -> 'Input':
        self.deadzone = deadzone
        return self

    def set_filter(self, axis_filter) -> 'Input':
        self.__filter = axis_filter
        return self

    def set_transform(self, axis_transform) -> 'Input':
        self.__transform = axis_transform
        return self

    def override(self, value):
        self.__current_value = value

    def wait_until(self, mode: str = 'press'):
        yield from ()
        if mode == 'press':
            while not self.get():
                yield None
        elif mode == 'up':
            while not self.get_button_up():
                yield None
        elif mode == 'down':
            while not self.get_button_down():
                yield None

    def __get_button__(self) -> bool:
        if self.__irl_mode__ == Input.BUTTON_MODE:
            return Input.__joysticks__[self.joystick_id].getRawButton(self.input_id)

        value = Input.__joysticks__[self.joystick_id].getRawAxis(self.input_id)
        value *= -1 if self.invert else 1

        return value > self.cutoff

    def __get_axis__(self) -> float:
        if self.__irl_mode__ == Input.AXIS_MODE:
            value = Input.__joysticks__[self.joystick_id].getRawAxis(self.input_id)
            value = frcmath.deadzone(value, self.deadzone)
            value = -value if self.invert else value
        else:
            value = Input.__joysticks__[self.joystick_id].getRawButton(self.input_id)
            value = value if value != self.invert else 0.

        return value

    def __get_composite_axis__(self) -> float:
        value = self.positive.get() - self.negative.get()
        return value

    def __evaluate_axis__(self, value):
        if self.__filter is not None:
            value = self.__filter(value)
        if self.__transform is not None:
            value = self.__transform(value)

        return value

    def initSendable(self, builder: wpiutil.SendableBuilder) -> None:
        if self.mode == Input.BUTTON_MODE:
            builder.addBooleanProperty('value', self.get, lambda v: None)
        else:
            builder.addDoubleProperty('value', self.get, lambda v: None)

    @staticmethod
    def __input_coroutine__():
        while True:
            for inp in Input.__inputs__.values():
                inp.__last_value = inp.__current_value

                if inp.mode == Input.AXIS_MODE:
                    inp.__current_value = inp.__get_axis__()
                elif inp.mode == Input.BUTTON_MODE:
                    inp.__current_value = inp.__get_button__()
                elif inp.mode == Input.COMPOSITE_AXIS_MODE:
                    inp.__current_value = inp.__get_composite_axis__()

            yield None

    @classmethod
    def add_button(cls,
                   name: str,
                   joystick_id: int,
                   input_id: str) -> 'Input':
        if name in cls.__inputs__:
            raise KeyError(f'Input "{name}" already exists.')

        button = cls(name, joystick_id, input_id, mode=cls.BUTTON_MODE)
        cls.__inputs__[name] = button

        return button

    @classmethod
    def add_axis(cls,
                 name: str,
                 joystick_id: int,
                 input_id: str,
                 inverted: bool = False,
                 deadzone: float = 0.1,
                 axis_filter=None,
                 axis_transform=None) -> 'Input':
        if name in cls.__inputs__:
            raise KeyError(f'Input "{name}" already exists.')

        axis = cls(name, joystick_id, input_id, mode=cls.AXIS_MODE, inverted=inverted, deadzone=deadzone, axis_filter=axis_filter, axis_transform=axis_transform)
        cls.__inputs__[name] = axis

        return axis

    @classmethod
    def create_composite_axis(cls,
                              name: str,
                              positive: 'Input',
                              negative: 'Input',
                              axis_filter=None,
                              axis_transform=None) -> 'Input':
        if name in cls.__inputs__:
            raise KeyError(f'Input "{name}" already exists.')

        composite = cls(name, mode=Input.COMPOSITE_AXIS_MODE, positive=positive, negative=negative, axis_filter=axis_filter, axis_transform=axis_transform)
        cls.__inputs__[name] = composite

        return composite

    @classmethod
    def get_input(cls, name):
        return cls.__inputs__[name]

    @classmethod
    def get_inputs(cls):
        return cls.__inputs__

    @staticmethod
    def init():
        Timer.start_coroutine(Input.__input_coroutine__(), CoroutineOrder.EARLY, ignore_stop_all=True)
