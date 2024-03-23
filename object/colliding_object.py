from vector import Vector
from .base import Object
# raise NotImplementedError()
class CollidingObject(Object):
    physics: bool
    def __init__(self, pos: Vector | tuple[int, int], size: Vector | tuple[int, int]) -> None:
        super().__init__(pos, size)
        self.physics = True
