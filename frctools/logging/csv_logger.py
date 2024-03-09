from frctools import Timer, CoroutineOrder
from datetime import datetime

import os


def stringify(data):
    if isinstance(data, float):
        return str(round(data, 3))

    return str(data)


class CSVLogger:
    __LOG_FOLDER__ = '/home/lvuser/pythonLog'

    def __init__(self, file_name: str):
        self.__init_time = Timer.get_current_time()
        self.data = [('time', lambda: Timer.get_elapsed(self.__init_time))]
        self.file_name = file_name

        self.__file = None
        self.__last_flush = 0

        self.__coroutine = None

    def init(self):
        if self.__file is not None:
            self.stop()

        now = datetime.now()

        self.__file = open(f'{CSVLogger.__LOG_FOLDER__}/{now.strftime("%m-%d-%y_%H:%M:%S")}_{self.file_name}.csv', 'a', buffering=0)
        self.__file.write('\t'.join([d[0] for d in self.data]) + '\n')

        self.__last_flush = Timer.get_current_time()

        self.__coroutine = Timer.start_coroutine(self.__log_loop__(), CoroutineOrder.LATE)

    def stop(self):
        self.__file.close()
        self.__file = None

        if not self.__coroutine.is_done:
            Timer.stop_coroutine(self.__coroutine)
            self.__coroutine = None

    def flush(self):
        self.__file.flush()
        self.__last_flush = Timer.get_current_time()

    def __log_loop__(self):
        while True:
            self.__file.write('\t'.join([stringify(d[1]()) for d in self.data]) + '\n')
            if Timer.get_elapsed(self.__last_flush) >= 0.25:
                self.__file.flush()
                self.__last_flush = Timer.get_current_time()

            yield None

    def add_data(self, name: str, data_source):
        self.data.append((name, data_source))

    @staticmethod
    def set_log_folder(folder: str):
        CSVLogger.__LOG_FOLDER__ = folder
        os.makedirs(folder, exist_ok=True)
