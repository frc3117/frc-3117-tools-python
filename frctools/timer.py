from enum import Enum, IntFlag
from typing import List

import time
import wpilib


class CoroutineOrder(int, Enum):
    EARLY = 0
    NORMAL = 1
    LATE = 2
    ALLWAYS = 3


class Coroutine:
    def __init__(self, generator, order, ignore_stop_all=False):
        self.__generator = generator
        self.order = order

        self.is_done = False
        self.ignore_stop_all = ignore_stop_all

    def do_coroutine(self):
        try:
            next(self.__generator)
        except StopIteration:
            self.is_done = True

    def wait(self):
        while not self.is_done:
            yield None

    def __iter__(self):
        yield from self.__generator


class Period(IntFlag):
    NONE =              0b00000000

    ENABLED =           0b00000001
    MANUAL =            0b00000010
    TEST =              0b00000100
    ENDGAME =           0b00001000

    AUTONOMOUS =        0b00000001
    AUTONOMOUS_TEST =   0b00000101
    TELEOP =            0b00000011
    TELEOP_TEST =       0b00000111
    TELEOP_ENDGAME =    0b00001011

    @property
    def is_enabled(self) -> bool:
        return self & Period.ENABLED == Period.ENABLED

    @is_enabled.setter
    def is_enabled(self, value: bool):
        return

    def has_flag(self, flag):
        return self & flag == flag


class ConcurrentEvent:
    class Block:
        def __init__(self, event: 'ConcurrentEvent'):
            self.__event = event
            self.__ready = False
            self.__consumed = False

        def set(self):
            self.__ready = True

        def is_ready(self):
            if self.__ready and not self.__consumed:
                self.__event.remove_block(self)
                self.__consumed = True

            return self.__ready

        def wait(self):
            yield from ()
            while not self.is_ready():
                yield None

        def __iter__(self):
            yield from self.wait()

    def __init__(self):
        self.__events = []

    def create_block(self):
        e = ConcurrentEvent.Block(self)
        self.__events.append(e)

        return e

    def remove_block(self, block):
        self.__events.remove(block)

    def set(self):
        for e in self.__events:
            e.set()


class Timer:
    __START_TIME = 0.
    __LAST_TIME = 0.

    __DT = 0.
    __FRAME_COUNT = 0

    __EARLY_COROUTINES: List['Coroutine'] = []
    __NORMAL_COROUTINES: List['Coroutine'] = []
    __LATE_COROUTINE: List['Coroutine'] = []

    __ALLWAYS_COROUTINES: List['Coroutine'] = []

    @staticmethod
    def init():
        Timer.__START_TIME = Timer.get_current_time()
        Timer.__LAST_TIME = Timer.__START_TIME

        Timer.__DT = 0.
        Timer.__FRAME_COUNT = 0

    @staticmethod
    def reset():
        Timer.__START_TIME = 0.
        Timer.__FRAME_COUNT = 0

        Timer.stop_all_coroutine()

    @staticmethod
    def evaluate():
        curr = Timer.get_current_time()

        Timer.__DT = (curr - Timer.__LAST_TIME)
        Timer.__LAST_TIME = curr

        Timer.__FRAME_COUNT += 1

    @staticmethod
    def start_coroutine(coroutine, order: CoroutineOrder = CoroutineOrder.NORMAL, ignore_stop_all: bool = False) -> Coroutine:
        cor = Coroutine(coroutine, order, ignore_stop_all)

        if order == CoroutineOrder.EARLY:
            Timer.__EARLY_COROUTINES.append(cor)
        elif order == CoroutineOrder.NORMAL:
            Timer.__NORMAL_COROUTINES.append(cor)
        elif order == CoroutineOrder.LATE:
            Timer.__LATE_COROUTINE.append(cor)
        elif order == CoroutineOrder.ALLWAYS:
            Timer.__ALLWAYS_COROUTINES.append(cor)

        return cor

    @staticmethod
    def start_coroutine_if_stopped(coroutine, ref_coroutine: Coroutine, order: CoroutineOrder = CoroutineOrder.NORMAL, ignore_stop_all: bool = False) -> Coroutine:
        if ref_coroutine is None or ref_coroutine.is_done:
            return Timer.start_coroutine(coroutine(), order, ignore_stop_all)

        return ref_coroutine

    @staticmethod
    def stop_coroutine(coroutine: Coroutine):
        if coroutine.order == CoroutineOrder.EARLY:
            Timer.__EARLY_COROUTINES.remove(coroutine)
        elif coroutine.order == CoroutineOrder.NORMAL:
            Timer.__NORMAL_COROUTINES.remove(coroutine)
        elif coroutine.order == CoroutineOrder.LATE:
            Timer.__LATE_COROUTINE.remove(coroutine)
        elif coroutine.order == CoroutineOrder.ALLWAYS:
            Timer.__ALLWAYS_COROUTINES.remove(coroutine)

        coroutine.is_done = True

    @staticmethod
    def stop_all_coroutine():
        for cor in Timer.__EARLY_COROUTINES:
            if not cor.ignore_stop_all:
                cor.is_done = True
                Timer.__EARLY_COROUTINES.remove(cor)

        for cor in Timer.__NORMAL_COROUTINES:
            if not cor.ignore_stop_all:
                cor.is_done = True
                Timer.__NORMAL_COROUTINES.remove(cor)

        for cor in Timer.__LATE_COROUTINE:
            if not cor.ignore_stop_all:
                cor.is_done = True
                Timer.__LATE_COROUTINE.remove(cor)

        for cor in Timer.__ALLWAYS_COROUTINES:
            if not cor.ignore_stop_all:
                cor.is_done = True
                Timer.__ALLWAYS_COROUTINES.remove(cor)

    @staticmethod
    def __do_coroutines__(coroutines: List[Coroutine]):
        try:
            for cor in coroutines:
                cor.do_coroutine()
                if cor.is_done:
                    coroutines.remove(cor)
        except Exception as e:
            print(e)

    @staticmethod
    def do_early_coroutines():
        Timer.__do_coroutines__(Timer.__EARLY_COROUTINES)

    @staticmethod
    def do_coroutines():
        Timer.__do_coroutines__(Timer.__NORMAL_COROUTINES)

    @staticmethod
    def do_late_coroutines():
        Timer.__do_coroutines__(Timer.__LATE_COROUTINE)

    @staticmethod
    def do_allways_coroutines():
        Timer.__do_coroutines__(Timer.__ALLWAYS_COROUTINES)

    @staticmethod
    def get_period() -> Period:
        period = Period.NONE

        if wpilib.DriverStation.isEnabled():
            period = period & Period.ENABLED

            if wpilib.DriverStation.isTest():
                period = period & Period.TEST
            if not wpilib.DriverStation.isAutonomous():
                period = period & Period.MANUAL

                if wpilib.DriverStation.getMatchTime() <= 20:
                    period = period & Period.ENDGAME

        return period

    @staticmethod
    def is_enabled():
        return wpilib.DriverStation.isEnabled()

    @staticmethod
    def is_auto():
        return wpilib.DriverStation.isAutonomous()

    @staticmethod
    def is_teleop():
        return wpilib.DriverStation.isTeleop()

    @staticmethod
    def get_delta_time():
        return Timer.__DT

    @staticmethod
    def get_current_field_time():
        return wpilib.Timer.getMatchTime()

    @staticmethod
    def get_current_time():
        return time.time_ns() / 1e9

    @staticmethod
    def get_time_since_start():
        return Timer.get_elapsed(Timer.__START_TIME)

    @staticmethod
    def get_elapsed(time: float):
        return Timer.get_current_time() - time

    @staticmethod
    def get_elapsed_frame(frame: int):
        return Timer.get_frame_count() - frame

    @staticmethod
    def get_frame_count():
        return Timer.__FRAME_COUNT

    @staticmethod
    def wait_for_frame(frame: int):
        if frame <= 0:
            yield from ()

        start_frame = Timer.get_frame_count()
        while Timer.get_elapsed_frame(start_frame) < frame:
            yield None

    @staticmethod
    def wait_for_seconds(seconds: float):
        if seconds <= 0.:
            yield from ()

        start_time = Timer.get_current_time()
        while Timer.get_elapsed(start_time) < seconds:
            yield None

    @staticmethod
    def wait_parallel(*coroutines):
        yield from ()
        cor_ls = [[True, x] for x in coroutines]

        still_running = True
        while still_running:
            still_running = False
            for cor in cor_ls:
                if cor[0]:
                    try:
                        next(cor[1])
                        still_running = True
                    except StopIteration:
                        cor[0] = False

            if still_running:
                yield None
