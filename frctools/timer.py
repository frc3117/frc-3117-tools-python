from enum import Enum
from typing import List

import time


class CoroutineOrder(int, Enum):
    EARLY = 0
    NORMAL = 1
    LATE = 2


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

    def __iter__(self):
        yield from self.__generator


class Timer:
    __START_TIME = 0.
    __LAST_TIME = 0.

    __DT = 0.
    __FRAME_COUNT = 0

    __EARLY_COROUTINES: List['Coroutine'] = []
    __NORMAL_COROUTINES: List['Coroutine'] = []
    __LATE_COROUTINE: List['Coroutine'] = []

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

        return cor

    @staticmethod
    def start_coroutine_if_stopped(coroutine, ref_coroutine: Coroutine, order: CoroutineOrder = CoroutineOrder.NORMAL) -> Coroutine:
        if ref_coroutine is None or ref_coroutine.is_done:
            return Timer.start_coroutine(coroutine(), order)

        return ref_coroutine

    @staticmethod
    def stop_coroutine(coroutine: Coroutine):
        if coroutine.order == CoroutineOrder.EARLY:
            Timer.__EARLY_COROUTINES.remove(coroutine)

        if coroutine.order == CoroutineOrder.NORMAL:
            Timer.__NORMAL_COROUTINES.remove(coroutine)

        if coroutine.order == CoroutineOrder.LATE:
            Timer.__LATE_COROUTINE.remove(coroutine)

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

        Timer.__EARLY_COROUTINES.clear()
        Timer.__NORMAL_COROUTINES.clear()
        Timer.__LATE_COROUTINE.clear()

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
    def get_delta_time():
        return Timer.__DT

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
    def get_frame_count():
        return Timer.__FRAME_COUNT

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
