from frctools import Timer, CoroutineOrder


class AutonomousManager:
    def __init__(self):
        self.__current_auto = None

    def start_auto(self, auto):
        if auto is None:
            return

        self.__current_auto = auto
        Timer.start_coroutine(self.__auto_loop__())

    def __auto_loop__(self):
        self.__current_auto.on_start()
        yield from self.__current_auto
        self.__current_auto.on_end()

    def end_auto(self):
        if self.__current_auto is not None and self.__current_auto.is_running():
            self.__current_auto.on_end()

        self.__current_auto = None