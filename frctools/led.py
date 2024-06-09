import math
import time

from frctools import Component, Timer, CoroutineOrder
from frctools.frcmath import repeat

import wpilib
import wpiutil


class LED(Component):
    def __init__(self, channel: int, led_count: int, idle_color=(255, 0, 0), brightness = 0.5):
        super().__init__()

        self.__led = wpilib.AddressableLED(channel)
        self.__data = [wpilib.AddressableLED.LEDData() for _ in range(led_count)]

        self.__led.setLength(led_count)
        self.__led.setData(self.__data)
        self.__led.start()

        self.__idle_color = idle_color
        self.__current_color = idle_color
        self.__brightness = brightness
        self.__priority = -1

        self.__coroutine = None

    def update(self):
        self.__coroutine = Timer.start_coroutine_if_stopped(self.__loop__, self.__coroutine, CoroutineOrder.LATE)

    def set_color(self, color, priority: int):
        if priority > self.__priority:
            self.__current_color = color
            self.__priority = priority

    def set_brightness(self, brightness: float):
        self.__brightness = brightness

    def get_brightness(self):
        return self.__brightness

    def __loop__(self):
        while True:
            self.__current_color = (
                int(self.__current_color[0] * self.__brightness),
                int(self.__current_color[1] * self.__brightness),
                int(self.__current_color[2] * self.__brightness)
            )

            for data in self.__data:
                data.setRGB(*self.__current_color)

            self.__led.setData(self.__data)

            self.__current_color = self.__idle_color
            self.__priority = -1
            yield None

    def initSendable(self, builder: wpiutil.SendableBuilder):
        builder.addDoubleProperty('brigthness', self.get_brightness, self.set_brightness)
