from typing import Dict
from wpilib import Joystick

from frctools import frcmath


class Input:
    BUTTON_MODE = 0
    AXIS_MODE = 1

    __joysticks__: Dict[int, Joystick] = {}
    __inputs__: Dict[str, 'Input'] = {}

    def __init__(self, name: str, joystick_id: int, input_id: str, mode: int):
        self.name = name
        self.joystick_id = joystick_id

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

        self.mode = mode

        self.deadzone = 0.1
        self.invert = False

        self.cutoff = 0.5
        self.click_value = 1.0

    def get(self) -> bool | float:
        if self.mode == Input.BUTTON_MODE:
            return self.__get_button__()
        elif self.mode == Input.AXIS_MODE:
            return self.__get_axis__()

    def __get_button__(self) -> bool:
        if self.__irl_mode__ == Input.BUTTON_MODE:
            return Input.__joysticks__[self.joystick_id].getRawButton(self.input_id)

        value = Input.__joysticks__[self.joystick_id].getRawAxis(self.input_id)
        value *= -1 if self.invert else 1

        return value > self.cutoff

    def __get_axis__(self) -> float:
        if self.__irl_mode__ == Input.AXIS_MODE:
            value = Input.__joysticks__[self.joystick_id].getRawAxis(self.input_id)
            return frcmath.deadzone(value, self.deadzone)

        value = Input.__joysticks__[self.joystick_id].getRawButton(self.input_id)
        value *= -self.click_value if self.invert else self.click_value

        return value

    @classmethod
    def add_button(cls, name: str, joystick_id: int, input_id: str) -> 'Input':
        if name in cls.__inputs__:
            raise KeyError(f'Input "{name}" already exists.')

        button = cls(name, joystick_id, input_id, cls.BUTTON_MODE)
        cls.__inputs__[name] = button

        return button

    @classmethod
    def add_axis(cls, name: str, joystick_id: int, input_id: str) -> 'Input':
        if name in cls.__inputs__:
            raise KeyError(f'Input "{name}" already exists.')

        axis = cls(name, joystick_id, input_id, cls.AXIS_MODE)
        cls.__inputs__[name] = axis

        return axis
