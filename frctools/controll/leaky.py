class LeakyIntegrator:
    def __init__(self, start_value: float = 0):
        self.__current_value = start_value

    def evaluate(self, value: float, l):
        self.__current_value = l * self.__current_value + (1 - l) * value
        return self.__current_value

    @property
    def current(self) -> float:
        return self.__current_value
    @current.setter
    def current(self, value: float):
        self.__current_value = value
