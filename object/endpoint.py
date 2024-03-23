import pygame

import asset
from vector import Vector
from .colliding_object import CollidingObject

class Endpoint(CollidingObject):
    def __init__(self, pos: Vector | tuple[int, int], size: Vector | tuple[int, int]) -> None:
        super().__init__(pos, size)

        self.physics = False

        path = asset.get_asset_path(asset.AssetType.ITEM, asset.ItemType.CHECKPOINT, asset.CheckpointType.END, asset.Checkpoint_EndVariant.IDLE)

        im = pygame.image.load(path).convert()

        self.image.blit(pygame.transform.scale(im, size), (0, 0))

        self.mask = pygame.mask.from_surface(self.image)

        self.col_listener = lambda: None

    def collides_with(self, player):
        self.col_listener()