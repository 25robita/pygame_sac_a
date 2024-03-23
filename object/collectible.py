from time import time

import pygame

import asset
from vector import Vector

from .colliding_object import CollidingObject

class Collectible(CollidingObject):
    def __init__(self, pos: Vector | tuple[int, int], size: Vector | tuple[int, int], asset_slices: int, *asset_specifiers: str) -> None:
        super().__init__(pos, size)
        self.physics = False

        path = asset.get_asset_path(*asset_specifiers)

        sheet = pygame.image.load(path).convert_alpha()

        self.sprites = []
        self.sprite_index = 0

        self.sprite_interval = 0.02
        self.prev_sprite = time()

        sprite_width = sheet.get_width() // asset_slices

        for i in range(asset_slices):
            s = pygame.Surface((sprite_width, sheet.get_height()), pygame.SRCALPHA, 32)
            s.blit(sheet, (0, 0), pygame.Rect(sprite_width * i, 0, sprite_width, sheet.get_height()))
            s = pygame.transform.scale(s, tuple(self.size))
            self.sprites.append(s)

    def increment_sprite(self):
        self.prev_sprite = time()
        self.sprite_index += 1
        self.sprite_index %= len(self.sprites)

        self.image = self.sprites[self.sprite_index]
        self.mask = pygame.mask.from_surface(self.image)


    def tick(self):
        if time() - self.prev_sprite >= self.sprite_interval:
            self.increment_sprite()
