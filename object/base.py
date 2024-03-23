import pygame
from pygame.sprite import Sprite

from vector import Vector

class Object(Sprite):
    def __init__(self, pos: Vector | tuple[int, int], size: Vector | tuple[int, int]) -> None:
        super().__init__()

        self.rect = pygame.Rect(*pos, *size)
        self.image = pygame.Surface(size, pygame.SRCALPHA, 32)

        self.size = Vector(*size)
        self.parent = None

    def adopt(self, level_manager):
        if self.parent:
            self.parent.emancipate(self)
        self.parent = level_manager

    def draw(self, surface: pygame.Surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))

    def tick(self):
        pass

    def collides_with(self, player):
        pass