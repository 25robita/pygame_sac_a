from typing import Self
from math import sqrt, ceil, floor
from random import random

class Vector:
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    def __iter__(self):
        yield self.x
        yield self.y

    def __repr__(self) -> str:
        return f"Vector ({self.x}, {self.y})"

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"
    
    def __abs__(self) -> float:
        return sqrt(self.x ** 2 + self.y ** 2)
    
    def __add__(self, other: Self | float | int) -> Self:
        if isinstance(other, Vector):
            return Vector(self.x + other.x, self.y + other.y)
        
        return Vector(self.x + other, self.y + other)

    def __ceil__(self):
        return Vector(ceil.x, ceil.y)
    
    def __eq__(self, other: Self) -> bool:
        return self.x == other.x and self.y == other.y
    
    def __floor__(self) -> Self:
        return Vector(floor(self.x), floor(self.y))
    
    def __floordiv__(self, other: Self | float | int) -> Self:
        if isinstance(other, Vector):
            return Vector(self.x // other.x, self.y // other.y)
        return Vector(self.x // other, self.y // other)
    
    def __ge__(self, other: Self | float | int) -> bool:
        return abs(self) >= abs(other)
    
    def __gt__(self, other: Self | float | int) -> bool:
        return abs(self) > abs(other)
    
    def __le__(self, other: Self | float | int) -> bool:
        return abs(self) <= abs(other)
    
    def __lt__(self, other: Self | float | int) -> bool:
        return abs(self) < abs(other)
    
    def __mod__(self, other: Self | float | int) -> Self:
        if isinstance(other, Vector):
            return Vector(self.x % other.x, self.y % other.y)
        
    def __mul__(self, other: Self | float | int) -> Self:
        if isinstance(other, Vector):
            return Vector(self.x * other.x, self.y * other.y)
        return Vector(self.x * other, self.y * other)
    
    def __ne__(self, other: Self) -> bool:
        return self.x != other.x or self.y != other.y
    
    def __neg__(self) -> Self:
        return Vector(self.x.__neg__(), self.y.__neg__())
    
    def __pos__(self) -> Self:
        return Vector(self.x.__pos__(), self.y.__neg__())
    
    def __pow__(self, other: Self | float | int) -> Self:
        if isinstance(other, Vector):
            return Vector(self.x ** other.x, self.y ** other.y)
        return Vector(self.x ** other, self.y ** other)
        
    def __radd__(self, other: Self | float | int) -> Self:
        return self.__add__(other)
    
    def __rsub__(self, other: Self | float | int) -> Self:
        if isinstance(other, Vector):
            return Vector(other.x - self.x, other.y - self.y)
        return Vector(other - self.x, other - self.y)
    
    def __rpow__(self, other: Self | float | int) -> Self:
        if isinstance(other, Vector):
            return Vector(other.x ** self.x, other.y ** self.y)
        return Vector(other ** self.x, other ** self.y)
    
    def __rfloordiv__(self, other: Self | float | int) -> Self:
        if isinstance(other, Vector):
            return Vector(other.x // self.x, other.y // self.y)
        return Vector(other // self.x, other // self.y)
    
    def __rmod__(self, other: Self | float | int) -> Self:
        if isinstance(other, Vector):
            return Vector(other.x % self.x, other.y % self.y)
        return Vector(other % self.x, other % self.y)
    
    def __rmul__(self, other: Self | float | int) -> Self:
        return self.__mul__(other)
    
    def __round__(self, arg: int | None = None) -> Self:
        if arg is not None:
            return Vector(self.x.__round__(arg), self.y.__round__(arg))
        return Vector(self.x.__round__(), self.y.__round__())
    
    def __rtruediv__(self, other: Self | float | int) -> Self:
        if isinstance(other, Vector):
            return Vector(other.x / self.x, other.y / self.y)
        return Vector(other / self.x, other / self.y)
    
    def __sub__(self, other: Self | float | int) -> Self:
        if isinstance(other, Vector):
            return Vector(self.x - other.x, self.y - other.y)
        return Vector(self.x - other, self.y - other)
    
    def __truediv__(self, other: Self | float | int) -> Self:
        if isinstance(other, Vector):
            return Vector(self.x / other.x, self.y / other.y)
        return Vector(self.x / other, self.y / other)
    
    def random_unit_vector():
        v = Vector(random()-.5, random()-.5)
        return v / abs(v)