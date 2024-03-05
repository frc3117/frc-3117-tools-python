from frctools import Timer, CoroutineOrder


class AutonomousSequence:
    def __init__(self):
        self.__is_running = False

    def on_start(self):
        self.__is_running = True

    def loop(self):
        yield None

    def on_end(self):
        self.__is_running = False

    def is_running(self):
        return self.__is_running

    def __iter__(self):
        yield from self.loop()
