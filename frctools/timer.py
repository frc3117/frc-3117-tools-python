from enum import Enum
from typing import List

import time


__START_TIME = 0.
__LAST_TIME = 0.

__DT = 0.
__FRAME_COUNT = 0

__EARLY_COROUTINES: List['Coroutine'] = []
__NORMAL_COROUTINES: List['Coroutine'] = []
__LATE_COROUTINE: List['Coroutine'] = []


class CoroutineOrder(int, Enum):
    EARLY = 0
    NORMAL = 1
    LATE = 2


class Coroutine:
    def __init__(self, generator, order):
        self.__generator = generator
        self.order = order

        self.is_done = False

    def do_coroutine(self):
        try:
            next(self.__generator)
        except StopIteration:
            self.is_done = True

    def __iter__(self):
        yield from self.__generator


class Timer:
    @staticmethod
    def init():
        global __START_TIME, __LAST_TIME, __DT, __FRAME_COUNT, __EARLY_COROUTINES, __NORMAL_COROUTINES, __LATE_COROUTINE

        __START_TIME = Timer.get_current_time()
        __LAST_TIME = __START_TIME

        __DT = 0.
        __FRAME_COUNT = 0

        __EARLY_COROUTINES = []
        __NORMAL_COROUTINES = []
        __LATE_COROUTINE = []

    @staticmethod
    def evaluate():
        global __START_TIME, __LAST_TIME, __DT, __FRAME_COUNT

        curr = Timer.get_current_time()

        __DT = (curr - __LAST_TIME)
        __LAST_TIME = curr

        __FRAME_COUNT += 1

    @staticmethod
    def start_coroutine(coroutine, order: CoroutineOrder = CoroutineOrder.NORMAL) -> Coroutine:
        cor = Coroutine(coroutine, order)

        if order == CoroutineOrder.EARLY:
            global __EARLY_COROUTINES
            __EARLY_COROUTINES.append(cor)
        elif order == CoroutineOrder.NORMAL:
            global __NORMAL_COROUTINES
            __NORMAL_COROUTINES.append(cor)
        elif order == CoroutineOrder.LATE:
            global __LATE_COROUTINE
            __LATE_COROUTINE.append(cor)

        return cor

    @staticmethod
    def stop_coroutine(coroutine: Coroutine):
        if coroutine.order == CoroutineOrder.EARLY:
            global __EARLY_COROUTINES
            __EARLY_COROUTINES.remove(coroutine)

        if coroutine.order == CoroutineOrder.NORMAL:
            global __NORMAL_COROUTINES
            __NORMAL_COROUTINES.remove(coroutine)

        if coroutine.order == CoroutineOrder.LATE:
            global __LATE_COROUTINE
            __LATE_COROUTINE.remove(coroutine)

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
        global __EARLY_COROUTINES
        Timer.__do_coroutines__(__EARLY_COROUTINES)

    @staticmethod
    def do_coroutines():
        global __NORMAL_COROUTINES
        Timer.__do_coroutines__(__NORMAL_COROUTINES)

    @staticmethod
    def do_late_coroutines():
        global __LATE_COROUTINE
        Timer.__do_coroutines__(__LATE_COROUTINE)

    @staticmethod
    def get_delta_time():
        global __DT
        return __DT

    @staticmethod
    def get_current_time():
        return time.time_ns() / 1e9

    @staticmethod
    def get_time_since_start():
        global __START_TIME
        return Timer.get_elapsed(__START_TIME)

    @staticmethod
    def get_elapsed(time: float):
        return Timer.get_current_time() - time

    @staticmethod
    def get_frame_count():
        global __FRAME_COUNT
        return __FRAME_COUNT

    @staticmethod
    def wait_for_frame(frame: int):
        start_frame = Timer.get_frame_count()
        while Timer.get_frame_count() - start_frame <= frame:
            yield None

    @staticmethod
    def wait_for_seconds(seconds: float):
        start_time = Timer.get_current_time()
        while Timer.get_current_time() - start_time <= seconds:
            yield None
