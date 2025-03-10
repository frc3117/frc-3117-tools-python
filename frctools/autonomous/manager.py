from frctools import Timer, CoroutineOrder, Coroutine


class AutonomousManager:
    def __init__(self):
        self.__current_auto = None
        self.__current_coroutine: Coroutine = None

    def start_auto(self, auto):
        if auto is None:
            return

        self.__current_auto = auto
        self.__current_coroutine = Coroutine(self.__auto_loop__(), None)

    def do_coroutine(self):
        if self.__current_coroutine is not None and not self.__current_coroutine.is_done:
            self.__current_coroutine.do_coroutine()

    def __auto_loop__(self):
        self.__current_auto.on_start()
        yield from self.__current_auto
        self.__current_auto.on_end()

    def end_auto(self):
        if self.__current_auto is not None and self.__current_auto.is_running():
            self.__current_auto.on_end()

        self.__current_auto = None