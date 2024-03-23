from math import ceil

import pygame

from vector import Vector
from .base import Object

class TileSheet(Object):
    def __init__(self, pos: Vector | tuple[int, int], size: Vector | tuple[int, int], tile: pygame.Surface | str) -> None:
        super().__init__(pos, size)

        self.tile_image = tile

        if isinstance(tile, str):
            self.tile_image = pygame.image.load(tile).convert_alpha()

        self.prev_camera_pos = Vector(0, 0)
        
        self.render()

    def render(self):
        """Renders the tile sheet and blits it to self.image"""
        width = ceil(self.rect.width / self.tile_image.get_width()) + 1
        height = ceil(self.rect.height / self.tile_image.get_height()) + 1

        self.image.fill((0, 0, 0, 0))

        tile_width, tile_height = self.tile_image.get_size()

        for x in range(-1, width):
            for y in range(-1, height):
                self.image.blit(self.tile_image, (x * self.tile_image.get_width() - (self.prev_camera_pos.x % tile_width), y * self.tile_image.get_height() - (self.prev_camera_pos.y % tile_height)))

    def tick(self):
        if self.parent.camera_position != self.prev_camera_pos:
            self.prev_camera_pos = Vector(*self.parent.camera_position)
            self.render()

    def draw(self, surface: pygame.Surface):
        surface.blit(self.image, (self.rect.x + self.prev_camera_pos.x, self.rect.y + self.prev_camera_pos.y))