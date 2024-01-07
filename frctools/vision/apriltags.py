from frctools.frcmath import Vector3, Quaternion


class AprilTag:
    def __init__(self, id: int, size: float, position: Vector3, rotation: Quaternion):
        self.__id = id
        self.__size = size
        self.__position = position
        self.__rotation = rotation

    @property
    def id(self):
        return self.__id

    @property
    def size(self):
        return self.__size

    @property
    def position(self):
        return self.__position

    @property
    def rotation(self):
        return self.rotation
