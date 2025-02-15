from frctools import Component, Timer, CoroutineOrder
from frctools.frcmath import lerp

import wpilib
import wpiutil


class LEDGroup:
    def __init__(self, led_data, idle_color):
        self.__led_data = led_data
        self.__current = idle_color
        self.__idle_color = idle_color
        self.__priority = -1

    def set_color(self, color, priority: int):
        if priority <= self.__priority:
            return

        self.__priority = priority
        self.__current = color

    def set_gradient(self, start_color, end_color, priority: int):
        if priority <= self.__priority:
            return

        self.__priority = priority

        l = len(self.__led_data)
        self.__current = []
        for i in range(l):
            p = i / l
            self.__current.append((
                lerp(start_color[0], end_color[0], p),
                lerp(start_color[1], end_color[1], p),
                lerp(start_color[2], end_color[2], p)
            ))

    def apply(self, brightness):
        if isinstance(self.__current, list):
            for c in self.__current:
                self.__led_data.setRGB(
                    int(c[0] * brightness),
                    int(c[1] * brightness),
                    int(c[2] * brightness)
                )
        else:
            color_b = (
                int(self.__current[0] * brightness),
                int(self.__current[1] * brightness),
                int(self.__current[2] * brightness)
            )

            for d in self.__led_data:
                d.setRGB(*color_b)

        self.__priority = -1
        self.__current = self.__idle_color


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

        self.__groups = {}

        self.__coroutine = None

    def update(self):
        self.__coroutine = Timer.start_coroutine_if_stopped(self.__loop__, self.__coroutine, CoroutineOrder.LATE)

    def set_color(self, color, priority: int):
        for group in self.__groups.values():
            group.set_color(color, priority)

    def set_brightness(self, brightness: float):
        self.__brightness = brightness

    def get_brightness(self):
        return self.__brightness

    def add_group(self, name: str, led_start: int, led_end: int):
        self.__groups[name] = LEDGroup(self.__data[led_start:led_end+1], self.__idle_color)
    def get_group(self, name):
        return self.__groups[name]

    def __loop__(self):
        while True:
            for group in self.__groups.values():
                group.apply(self.__brightness)

            self.__led.setData(self.__data)
            yield None

    def initSendable(self, builder: wpiutil.SendableBuilder):
        builder.addDoubleProperty('brigthness', self.get_brightness, self.set_brightness)
