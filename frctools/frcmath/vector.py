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
    # --- Vector Methods ---

    def sqr_magnitude(self) -> float:
        mag = 0
        for i in self:
            mag += i ** 2

        return mag

    def magnitude(self) -> float:
        return math.sqrt(self.sqr_magnitude())

    def normalized(self):
        return self / self.magnitude()

    def lerp(self, other, t: float):
        return self + (other - self) * t

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
        for i in range(len(self)):
            other_vec[i] += self[i]

        return self.__class__.from_list(other_vec)

    def __iadd__(self, other):
        other_vec = __get_vec_from_other__(len(self), other)
        for i in range(len(self)):
            self[i] += other_vec[i]

        return self

    def __sub__(self, other):
        other_vec = __get_vec_from_other__(len(self), other)
        for i in range(len(self)):
            other_vec[i] -= self[i]

        return self.__class__.from_list(other_vec)

    def __isub__(self, other):
        other_vec = __get_vec_from_other__(len(self), other)
        for i in range(len(self)):
            self[i] -= other_vec[i]

        return self

    def __mul__(self, other):
        other_vec = __get_vec_from_other__(len(self), other)
        for i in range(len(self)):
            other_vec[i] *= self[i]

        return self.__class__.from_list(other_vec)

    def __imul__(self, other):
        other_vec = __get_vec_from_other__(len(self), other)
        for i in range(len(self)):
            self[i] *= other_vec[i]

        return self

    def __truediv__(self, other):
        other_vec = __get_vec_from_other__(len(self), other)
        for i in range(len(self)):
            other_vec[i] /= self[i]

        return self.__class__.from_list(other_vec)

    def __itruediv__(self, other):
        other_vec = __get_vec_from_other__(len(self), other)
        for i in range(len(self)):
            self[i] /= other_vec[i]

        return self

    def __getitem__(self, item):
        raise NotImplementedError()

    def __setitem__(self, key, value):
        raise NotImplementedError()

    def __iter__(self):
        for i in range(len(self)):
            yield self[i]

    def __len__(self):
        raise NotImplementedError()

    def __str__(self):
        str_list = [str(i) for i in self]
        return f'({", ".join(str_list)})'

    def __repr__(self):
        return f"{type(self)}({str(self)})"


class Vector2(VectorBase):
    def __init__(self, x: float = 0, y: float = 0):
        self.x = float(x)
        self.y = float(y)

    # --- Vector Methods ---
    def dot(self, other: 'Vector2') -> float:
        return self.x * other.x + self.y * other.y

    def angle(self, other: 'Vector2') -> float:
        return math.acos(self.dot(other) / (self.magnitude() * other.magnitude()))

    # --- Operators Overloads ---

    def __getitem__(self, item):
        if isinstance(item, slice):
            return [self[i] for i in range(len(self))[item]]

        if item == 0:
            return self.x
        elif item == 1:
            return self.y

        raise IndexError(f"Index {item} out of range for Vector2.")

    def __setitem__(self, key, value):
        if key == 0:
            self.x = value
        elif key == 1:
            self.y = value
        else:
            raise IndexError(f"Index {key} out of range for Vector2.")

    def __len__(self):
        return 2


class Vector3(VectorBase):
    def __init__(self, x: float = 0, y: float = 0, z: float = 0):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)

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
        return math.acos(self.dot(other) / (self.magnitude() * other.magnitude()))

    # --- Operators Overloads ---

    def __getitem__(self, item):
        if isinstance(item, slice):
            return [self[i] for i in range(len(self))[item]]

        if item == 0:
            return self.x
        elif item == 1:
            return self.y
        elif item == 2:
            return self.z

        raise IndexError(f"Index {item} out of range for Vector3.")

    def __setitem__(self, key, value):
        if key == 0:
            self.x = value
        elif key == 1:
            self.y = value
        elif key == 2:
            self.z = value
        else:
            raise IndexError(f"Index {key} out of range for Vector3.")

    def __len__(self):
        return 3


class Vector4(VectorBase):
    def __init__(self, x: float = 0, y: float = 0, z: float = 0, w: float = 0):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)
        self.w = float(w)

    # --- Vector Methods ---

    # --- Operators Overloads ---

    def __getitem__(self, item):
        if isinstance(item, slice):
            return [self[i] for i in range(len(self))[item]]

        if item == 0:
            return self.x
        elif item == 1:
            return self.y
        elif item == 2:
            return self.z
        elif item == 3:
            return self.w

        raise IndexError(f"Index {item} out of range for Vector4.")

    def __setitem__(self, key, value):
        if key == 0:
            self.x = value
        elif key == 1:
            self.y = value
        elif key == 2:
            self.z = value
        elif key == 3:
            self.w = value
        else:
            raise IndexError(f"Index {key} out of range for Vector4.")

    def __len__(self):
        return 4


class Quaternion(VectorBase):
    def __init__(self, x: float, y: float, z: float, w: float):
        self.x = x
        self.y = y
        self.z = z
        self.w = w

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

    # TODO: Add Custom Quaternion Operators

    def __getitem__(self, item):
        if isinstance(item, slice):
            return [self[i] for i in range(len(self))[item]]

        if item == 0:
            return self.x
        elif item == 1:
            return self.y
        elif item == 2:
            return self.z
        elif item == 3:
            return self.w

        raise IndexError(f"Index {item} out of range for Quaternion.")

    def __setitem__(self, key, value):
        if key == 0:
            self.x = value
        elif key == 1:
            self.y = value
        elif key == 2:
            self.z = value
        elif key == 3:
            self.w = value
        else:
            raise IndexError(f"Index {key} out of range for Quaternion.")

    def __len__(self):
        return 4


class Polar:
    def __init__(self, theta, radius):
        self.theta = theta
        self.radius = radius

    @staticmethod
    def from_vector(vec) -> 'Polar':
        return Polar(math.atan2(vec.y, vec.x),
                     vec.magnitude())

    def to_vector(self) -> Vector2:
        return Vector2(self.radius * math.cos(self.theta),
                       self.radius * math.sin(self.theta))

    def rotate(self, angle):
        self.theta += angle
        self.theta %= math.tau
