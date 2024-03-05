from statistics import mean


class MovingAverage:
    def __init__(self, max_size):
        self.__max_size = max_size
        self.__queue = []

        self.__last_avg = 0

    def evaluate(self, new_val):
        self.__queue.append(new_val)
        if len(self.__queue) > self.__max_size:
            self.__queue.pop(0)

        self.__last_avg = mean(self.__queue)
        return self.__last_avg

    def get(self):
        return self.__last_avg

    def clear(self):
        self.__queue.clear()
