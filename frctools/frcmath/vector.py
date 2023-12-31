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
    def __init__(self, x: float, y: float):
        self.x = float(x)
        self.y = float(y)

    # --- Vector Methods ---
    def dot(self, other: 'Vector2') -> float:
        return self.x * other.x + self.y * other.y

    def angle(self, other: 'Vector2') -> float:
        return math.acos(self.dot(other) / (self.magnitude() * other.magnitude()))

    # --- Operators Overloads ---

    def __getitem__(self, item):
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
    def __init__(self, x: float, y: float, z: float):
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
