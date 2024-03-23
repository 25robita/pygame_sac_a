import pygame

from vector import Vector
from .colliding_object import CollidingObject
import asset

class Block(CollidingObject):
    def __init__(self, pos: Vector | tuple[int, int], size: Vector | tuple[int, int] = Vector(48, 48), asset_x: int = 0, asset_y: int = 1) -> None:
        super().__init__(pos, size)

        image = pygame.image.load(asset.get_asset_path(asset.AssetType.TERRAIN, asset.TERRAIN)).convert_alpha()

        self.image.blit(
            pygame.transform.scale(image, tuple(Vector(image.get_width(), image.get_height()) * self.size / 48)),
            (0, 0),
            pygame.Rect(asset_x * self.size.x / 48 * 64, asset_y * self.size.y / 48 * 64, *size)
        )

        self.update()

    def update(self):
        self.mask = pygame.mask.from_surface(self.image)