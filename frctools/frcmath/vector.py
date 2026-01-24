from .math import angle_normalize


from wpimath.geometry import Translation2d, Translation3d


from typing import Tuple, List

import math


def __get_vec_from_other__(length: int, other) -> List[float]:
    if isinstance(other, (int, float)):
        return [other] * length

    if isinstance(other, (list, VectorBase)):
        return other[:length]

    if isinstance(other, tuple):
        return list(other[:length])


class VectorBase:
    def __init__(self, *args):
        self.__list = list(args)

        self.__sqr_magnitude = 0.
        self.__magnitude = 0.

        self.__refresh_magnitude__()

    # --- Vector Methods ---

    def __refresh_sqr_magnitude__(self):
        mag = 0
        for val in self:
            mag += val * val

        self.__sqr_magnitude = mag

    @property
    def sqr_magnitude(self) -> float:
        return self.__sqr_magnitude

    def __refresh_magnitude__(self):
        self.__refresh_sqr_magnitude__()
        self.__magnitude = math.sqrt(self.__sqr_magnitude)

    @property
    def magnitude(self) -> float:
        return self.__magnitude

    def normalize(self):
        for i in range(len(self)):
            self[i] /= self.magnitude

        self.__magnitude = 1.
        self.__sqr_magnitude = 1.

        return self

    def normalized(self):
        copy = self.copy()
        copy.normalize()

        return copy

    def lerp(self, other, t: float):
        return self + (other - self) * t

    def copy(self):
        return self.__class__(*iter(self))

    @classmethod
    def from_tuple(cls, tup):
        return cls(*tup)

    def to_tuple(self) -> Tuple:
        return tuple(self)

    @classmethod
    def from_list(cls, lst):
        return cls(*lst)

    def to_list(self) -> List:
        return list(self)

    # --- Operators Overloads ---

    def __add__(self, other):
        other_vec = __get_vec_from_other__(len(self), other)
        new_vec = self.__class__(0., 0., 0.)
        for i in range(len(self)):
            new_vec[i] = self[i] + other_vec[i]

        new_vec.__refresh_magnitude__()
        return new_vec

    def __iadd__(self, other):
        other_vec = __get_vec_from_other__(len(self), other)
        for i in range(len(self)):
            self[i] += other_vec[i]

        return self

    def __sub__(self, other):
        other_vec = __get_vec_from_other__(len(self), other)
        new_vec = self.__class__(0., 0., 0.)
        for i in range(len(self)):
            new_vec[i] = self[i] - other_vec[i]

        new_vec.__refresh_magnitude__()
        return new_vec

    def __isub__(self, other):
        other_vec = __get_vec_from_other__(len(self), other)
        for i in range(len(self)):
            self[i] -= other_vec[i]

        return self

    def __mul__(self, other):
        other_vec = __get_vec_from_other__(len(self), other)
        new_vec = self.__class__(0., 0., 0.)
        for i in range(len(self)):
            new_vec[i] = self[i] * other_vec[i]

        new_vec.__refresh_magnitude__()
        return new_vec

    def __imul__(self, other):
        other_vec = __get_vec_from_other__(len(self), other)
        for i in range(len(self)):
            self[i] *= other_vec[i]

        return self

    def __truediv__(self, other):
        other_vec = __get_vec_from_other__(len(self), other)
        new_vec = self.__class__(0., 0., 0.)
        for i in range(len(self)):
            new_vec[i] = self[i] / other_vec[i]

        new_vec.__refresh_magnitude__()
        return new_vec

    def __itruediv__(self, other):
        other_vec = __get_vec_from_other__(len(self), other)
        for i in range(len(self)):
            self[i] /= other_vec[i]

        return self

    def __getitem__(self, item):
        return self.__list[item]

    def __setitem__(self, key, value):
        self.__list[key] = value

    def __iter__(self):
        yield from self.__list

    def __len__(self):
        raise NotImplementedError()

    def __str__(self):
        str_list = [str(i) for i in self]
        return f'({", ".join(str_list)})'

    def __repr__(self):
        return f"{type(self)}({str(self)})"


class Range(VectorBase):
    def __init__(self, min: float, max: float):
        super().__init__(float(min), float(max))

    @property
    def min(self):
        return self[0]
    @min.setter
    def min(self, value: float):
        self[0] = value

    @property
    def max(self):
        return self[1]
    @max.setter
    def max(self, value: float):
        self[1] = value

    def __len__(self):
        return 2


class Vector2(VectorBase):
    def __init__(self, x: float = 0., y: float = 0.):
        super().__init__(float(x), float(y))

    # --- Vector Methods ---
    def dot(self, other: 'Vector2') -> float:
        return self.x * other.x + self.y * other.y

    def angle(self, other: 'Vector2') -> float:
        return math.acos(self.dot(other) / (self.magnitude * other.magnitude))

    def rotate(self, theta) -> 'Vector2':
        cos_t = math.cos(theta)
        sin_t = math.sin(theta)

        return Vector2(self.x * cos_t - self.y * sin_t,
                       self.x * sin_t + self.y * cos_t)

    # Constants
    @staticmethod
    def zero() -> 'Vector2':
        return Vector2(0, 0)

    @staticmethod
    def one() -> 'Vector2':
        return Vector2(1, 1)

    # --- Operators Overloads ---

    @property
    def x(self) -> float:
        return self[0]

    @x.setter
    def x(self, value: float):
        self[0] = value
        self.__refresh_magnitude__()

    @property
    def y(self) -> float:
        return self[1]

    @y.setter
    def y(self, value: float):
        self[1] = value
        self.__refresh_magnitude__()

    def __len__(self):
        return 2

    def to_translation2d(self) -> Translation2d:
        return Translation2d(self.x, self.y)


class Vector3(VectorBase):
    def __init__(self, x: float = 0., y: float = 0., z: float = 0.):
        super().__init__(float(x), float(y), float(z))

    # --- Vector Methods ---
    def dot(self, other: 'Vector3') -> float:
        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross(self, other: 'Vector3') -> 'Vector3':
        return Vector3(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x
        )

    def angle(self, other: 'Vector3') -> float:
        return math.acos(self.dot(other) / (self.magnitude * other.magnitude))

    # --- Operators Overloads ---
    @property
    def x(self) -> float:
        return self[0]

    @x.setter
    def x(self, value: float):
        self[0] = value
        self.__refresh_magnitude__()

    @property
    def y(self) -> float:
        return self[1]

    @y.setter
    def y(self, value: float):
        self[1] = value
        self.__refresh_magnitude__()

    @property
    def z(self) -> float:
        return self[2]

    @z.setter
    def z(self, value: float):
        self[2] = value
        self.__refresh_magnitude__()

    def __len__(self):
        return 3

    def to_translation3d(self) -> Translation3d:
        return Translation3d(self.x, self.y, self.z)


class Vector4(VectorBase):
    def __init__(self, x: float = 0, y: float = 0, z: float = 0, w: float = 0):
        super().__init__(float(x), float(y), float(z), float(w))

    # --- Vector Methods ---

    # --- Operators Overloads ---
    @property
    def x(self) -> float:
        return self[0]

    @x.setter
    def x(self, value: float):
        self[0] = value
        self.__refresh_magnitude__()

    @property
    def y(self) -> float:
        return self[1]

    @y.setter
    def y(self, value: float):
        self[1] = value
        self.__refresh_magnitude__()

    @property
    def z(self) -> float:
        return self[2]

    @z.setter
    def z(self, value: float):
        self[2] = value
        self.__refresh_magnitude__()

    @property
    def w(self) -> float:
        return self[3]

    @w.setter
    def w(self, value: float):
        self[3] = value
        self.__refresh_magnitude__()

    def __len__(self):
        return 4


class Quaternion(VectorBase):
    def __init__(self, x: float, y: float, z: float, w: float):
        super().__init__(float(x), float(y), float(z), float(w))

    @staticmethod
    def from_euler(euler) -> 'Quaternion':
        cr = math.cos(euler.x * 0.5)
        sr = math.sin(euler.x * 0.5)
        cp = math.cos(euler.y * 0.5)
        sp = math.sin(euler.y * 0.5)
        cy = math.cos(euler.z * 0.5)
        sy = math.sin(euler.z * 0.5)

        return Quaternion(sr * cp * cy - cr * sp * sy,
                          cr * sp * cy + sr * cp * sy,
                          cr * cp * sy - sr * sp * cy,
                          cr * cp * cy + sr * sp * sy)

    @property
    def euler(self) -> Vector3:
        sinr_cosp = 2 * (self.w * self.x + self.y * self.z)
        cosr_cosp = 1 - 2 * (self.x**2 + self.y**2)
        x = math.atan2(sinr_cosp, cosr_cosp)

        y_common = 2 * (self.w * self.y - self.x * self.z)
        sinp = math.sqrt(1 + y_common)
        cosp = math.sqrt(1 - y_common)
        y = math.atan2(sinp, cosp) - math.pi / 2

        siny_cosp = 2 * (self.w * self.z + self.x * self.y)
        cosy_cosp = 1 - 2 * (self.y**2 + self.z * self.y**2)
        z = math.atan2(siny_cosp, cosy_cosp)

        return Vector3(x, y, z)

    @staticmethod
    def from_rotation_matrix(mtx) -> 'Quaternion':
        quat = Quaternion(0, 0, 0, 0)

        trace = mtx[0][0] + mtx[1][1] + mtx[2][2]
        if trace > 0:
            trace = math.sqrt(trace + 1.0)
            quat.w = 0.5 * trace
            trace = 0.5 / trace

            quat.x = (mtx[2][1] - mtx[1][2]) * trace
            quat.y = (mtx[0][2] - mtx[2][0]) * trace
            quat.z = (mtx[1][0] - mtx[0][1]) * trace
        else:
            i = 0
            if mtx[1][1] > mtx[0][0]:
                i = 1
            if mtx[2][2] > mtx[i][i]:
                i = 2

            j = (i + 1) % 3
            k = (j + 1) % 3

            trace = math.sqrt(mtx[i][i] - mtx[j][j] - mtx[k][k] + 1)
            quat[i] = 0.5 * trace
            trace = 0.5 / trace

            quat[3]  = (mtx[k][j] - mtx[j][k]) * trace
            quat[j] = (mtx[j][i] - mtx[i][j]) * trace
            quat[k] = (mtx[k][i] - mtx[i][k]) * trace

        return quat

    # TODO: Add Custom Quaternion Operators

    @property
    def x(self) -> float:
        return self[0]

    @x.setter
    def x(self, value: float):
        self[0] = value
        self.__refresh_magnitude__()

    @property
    def y(self) -> float:
        return self[1]

    @y.setter
    def y(self, value: float):
        self[1] = value
        self.__refresh_magnitude__()

    @property
    def z(self) -> float:
        return self[2]

    @z.setter
    def z(self, value: float):
        self[2] = value
        self.__refresh_magnitude__()

    @property
    def w(self) -> float:
        return self[3]

    @w.setter
    def w(self, value: float):
        self[3] = value
        self.__refresh_magnitude__()

    @property
    def conjugate(self):
        norm = self.normalized()
        return Quaternion(-norm.x, -norm.y, -norm.z, norm.w)

    def __mul__(self, other):
        if isinstance(other, Quaternion):
            return Quaternion(
                (self.w * other.x) + (self.x * other.w) + (self.y * other.z) - (self.z * other.y),
                (self.w * other.y) - (self.x * other.z) + (self.y * other.w) + (self.z * other.x),
                (self.w * other.z) + (self.x * other.y) - (self.y * other.x) + (self.z * other.w),
                (self.w * other.w) - (self.x * other.x) - (self.y * other.y) - (self.z * other.z)
            )
        if isinstance(other, Vector3):
            q_conj = self.conjugate
            v_quat = Quaternion(other.x, other.y, other.z, 0)

            rot = (self * v_quat) * q_conj

            return Vector3(rot.x, rot.y, rot.z)

    def __len__(self):
        return 4


class Polar:
    def __init__(self, theta, radius):
        self.theta = theta
        self.radius = radius

    @staticmethod
    def from_vector(vec) -> 'Polar':
        return Polar(angle_normalize(math.atan2(vec.y, vec.x)),
                     vec.magnitude())

    def to_vector(self) -> Vector2:
        return Vector2(self.radius * math.cos(self.theta),
                       self.radius * math.sin(self.theta))

    def rotate(self, angle: float) -> 'Polar':
        self.theta = angle_normalize(self.theta + angle)
        return self

    def copy(self) -> 'Polar':
        return Polar(self.theta, self.radius)

    def __str__(self):
        return f'({self.radius}, {self.theta}°)'

    def __repr__(self):
        return f'Polar({str(self)})'
