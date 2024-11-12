from frctools.frcmath import Vector3, Quaternion


class AprilTagDefinition:
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


CRESCENDO_2024_APRIL_TAGS = {
    1: AprilTagDefinition(1, 165.1, Vector3(15.079472, 0.245872, 1.355852), Quaternion(0., 0., 0.8660254037844386, 0.5)),
    2: AprilTagDefinition(2, 165.1, Vector3(16.185134, 0.883666, 1.355852), Quaternion(0., 0., 0.8660254037844386, 0.5)),
    3: AprilTagDefinition(3, 165.1, Vector3(16.579342, 4.982718, 1.451102), Quaternion(0., 0., 1., 0.)),
    4: AprilTagDefinition(4, 165.1, Vector3(16.579342, 5.547868, 1.451102), Quaternion(0., 0., 1., 0.)),
    5: AprilTagDefinition(5, 165.1, Vector3(14.700758, 8.2042, 1.355852), Quaternion(0., 0., 0.7071067811865476, -0.7071067811865475)),
    6: AprilTagDefinition(6, 165.1, Vector3(1.8415, 8.2042, 1.355852), Quaternion(0., 0., 0.7071067811865476, -0.7071067811865475)),
    7: AprilTagDefinition(7, 165.1, Vector3(-0.0381, 5.547868, 1.451102), Quaternion(0., 0., 0., 1.)),
    8: AprilTagDefinition(8, 165.1, Vector3(-0.0381, 4.982718, 1.451102), Quaternion(0., 0., 0., 1.)),
    9: AprilTagDefinition(9, 165.1, Vector3(0.356108, 0.883666, 1.355852), Quaternion(0., 0., 0.5, 0.8660254037844387)),
    10: AprilTagDefinition(10, 165.1, Vector3(1.461516, 0.245872, 1.355852), Quaternion(0., 0., 0.5, 0.8660254037844387)),
    11: AprilTagDefinition(11, 165.1, Vector3(11.904726, 3.713226, 1.3208), Quaternion(0., 0., 0.5, -0.8660254037844387)),
    12: AprilTagDefinition(12, 165.1, Vector3(11.904726, 4.49834, 1.3208), Quaternion(0., 0., 0.5, 0.8660254037844387)),
    13: AprilTagDefinition(13, 165.1, Vector3(11.220196, 4.105148, 1.3208), Quaternion(0., 0., 1., 0.)),
    14: AprilTagDefinition(14, 165.1, Vector3(5.320792, 4.105148, 1.3208), Quaternion(0., 0., 0., 1.)),
    15: AprilTagDefinition(15, 165.1, Vector3(4.641342, 4.49834, 1.3208), Quaternion(0., 0., 0.8660254037844386, 0.5)),
    16: AprilTagDefinition(16, 165.1, Vector3(4.641342, 3.713226, 1.3208), Quaternion(0., 0., 0.8660254037844386, -0.5)),
}
