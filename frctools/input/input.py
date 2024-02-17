from typing import Dict, Union
from enum import Enum
from wpilib import Joystick

from frctools import frcmath


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


class Input:
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
                 negative: 'Input' = None):
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

        self.__debounce = False

    def get(self) -> Union[bool, float]:
        if self.mode == Input.BUTTON_MODE:
            return self.__get_button__()
        elif self.mode == Input.AXIS_MODE:
            return self.__get_axis__()
        elif self.mode == Input.COMPOSITE_AXIS_MODE:
            return self.__get_composite_axis()

    def get_button_down(self) -> bool:
        button_val = self.__get_button__()
        if not button_val:
            self.__debounce = False
            return False

        if button_val and not self.__debounce:
            return True

        return False


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

            return -value if self.invert else value

        button = Input.__joysticks__[self.joystick_id].getRawButton(self.input_id)
        return button if button != self.invert else 0.

    def __get_composite_axis(self) -> float:
        return self.positive.get() - self.negative.get()

    @classmethod
    def add_button(cls, name: str, joystick_id: int, input_id: str) -> 'Input':
        if name in cls.__inputs__:
            raise KeyError(f'Input "{name}" already exists.')

        button = cls(name, joystick_id, input_id, cls.BUTTON_MODE)
        cls.__inputs__[name] = button

        return button

    @classmethod
    def add_axis(cls, name: str, joystick_id: int, input_id: str, inverted=False, deadzone=0.1) -> 'Input':
        if name in cls.__inputs__:
            raise KeyError(f'Input "{name}" already exists.')

        axis = cls(name, joystick_id, input_id, mode=cls.AXIS_MODE, inverted=inverted, deadzone=deadzone)
        cls.__inputs__[name] = axis

        return axis

    @classmethod
    def create_composite_axis(cls, name: str, positive: 'Input', negative: 'Input') -> 'Input':
        if name in cls.__inputs__:
            raise KeyError(f'Input "{name}" already exists.')

        composite = cls(name, mode=Input.COMPOSITE_AXIS_MODE, positive=positive, negative=negative)
        cls.__inputs__[name] = composite

        return composite

    @classmethod
    def get_input(cls, name):
        return cls.__inputs__[name]
