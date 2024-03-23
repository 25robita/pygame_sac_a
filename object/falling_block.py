from time import time

from vector import Vector
from .block import Block

class FallingBlock(Block):
    def __init__(self, pos: Vector | tuple[int, int], size: Vector | tuple[int, int] = ...) -> None:
        super().__init__(pos, size, 0, 0)

        self.falling = False
        self.will_fall_at = None

        self.y = self.rect.y
        self.prev_grav = time()
        self.fall_speed = 500

    def collides_with(self, player):
        self.will_fall_at = time() + 0.05

    def tick(self):
        if not self.falling:
            if self.will_fall_at is not None and time() > self.will_fall_at:
                self.falling = True
                self.prev_grav = time()
            return

        dt = time() - self.prev_grav
        self.prev_grav = time()

        self.y += dt * self.fall_speed
        self.rect.y = int(self.y)

        if self.y > 1000:
            self.parent.emancipate(self)