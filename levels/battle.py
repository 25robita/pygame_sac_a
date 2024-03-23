from typing import Literal
from time import time
from random import random, choice

import pygame

import asset
from vector import Vector
from .level_manager import LevelManager
from player import Player
from object import Object
from object.tile_sheet import TileSheet
from object.collectible import Collectible
from endscreen import endscreen

class Battle(LevelManager):
    def __init__(self, surface: pygame.Surface) -> None:
        super().__init__(surface)

        self.left: pygame.Surface | None = None
        """Used for player 1"""
        self.right: pygame.Surface | None = None
        """Used for player 2"""

        self.player1: Player | None = None
        self.player2: Player | None = None

        self.pixel_rate = 0.5
        self.prev_pix = time()

        self.pixel_left = 0
        self.pixel_right = 0

        self.camera_position_left = Vector(0, 0)
        self.camera_position_right = Vector(0, 0)

        self.left_objects: list[Object] = []
        self.right_objects: list[Object] = []

        self.scroll_tolerance = Vector(100, 64)

        self.lose_pix_amount = 20

    def reset(self):
        super().reset()
        self.pixel_left = 0
        self.pixel_right = 0

        self.camera_position_left = Vector(0, 0)
        self.camera_position_right = Vector(0, 0)

        self.left_objects = []
        self.right_objects = []

    def add_left(self, *objs: Object):
        for obj in objs:
            self.left_objects.append(obj)
            obj.adopt(self)

    def add_right(self, *objs: Object):
        for obj in objs:
            self.right_objects.append(obj)
            obj.adopt(self)

    @property
    def objects(self):
        return [*self.left_objects, *self.right_objects]
    
    @objects.setter
    def objects(self, value):
        return # should never be used anyway

    def start(self):
        self.left_objects = []
        self.right_objects = []

        self.prev_pix = time()

        self.left  = pygame.Surface((self.surface.get_width() // 2, self.surface.get_height()), pygame.SRCALPHA, 32)

        self.right = pygame.Surface((self.surface.get_width() // 2, self.surface.get_height()), pygame.SRCALPHA, 32)
        self.add_left(TileSheet((0,0), self.left.get_size(), asset.get_asset_path(asset.AssetType.BACKGROUND, asset.BackgroundType.BLUE)))
        self.add_right(TileSheet((0,0), self.right.get_size(), asset.get_asset_path(asset.AssetType.BACKGROUND, asset.BackgroundType.BLUE)))

        self.player1 = Player(self.left.get_rect().center, (48, 48), self.key_listener, asset.CharacterType.MASK_DUDE)
        self.player1.top_down = True
        self.player1.left_key = pygame.K_a
        self.player1.right_key = pygame.K_d
        self.player1.up_key = pygame.K_w
        self.player1.down_key = pygame.K_s
        self.player1.jump_key = pygame.K_LMETA # i don't need these but idk why not ig
        self.add_left(self.player1)

        self.player2 = Player(self.right.get_rect().center, (48, 48), self.key_listener, asset.CharacterType.PINK_MAN)
        self.player2.top_down = True
        self.player2.jump_key = pygame.K_RMETA # i don't need these but idk why not ig
        self.add_right(self.player2)

    def pix(self):
        """Pixelates each surface the respective amount"""
        if self.pixel_left > 2:
            s = pygame.transform.scale(pygame.transform.scale_by(self.left, 1/int(self.pixel_left)), self.left.get_size())
            self.left.blit(s, (0, 0))

        if self.pixel_right > 2:
            s = pygame.transform.scale(pygame.transform.scale_by(self.right, 1/int(self.pixel_right)), self.right.get_size())
            self.right.blit(s, (0, 0))

    def emancipate(self, obj: Object):
        if obj in self.left_objects:
            self.left_objects.remove(obj)
        if obj in self.right_objects:
            self.right_objects.remove(obj)

    def draw(self):
        for obj in self.left_objects:
            obj.draw(_SfcPartial(self.camera_position_left, self.left))

        for obj in self.right_objects:
            obj.draw(_SfcPartial(self.camera_position_right, self.right))

        self.pix()

        self.surface.blit(self.left, (0, 0))
        self.surface.blit(self.right, (self.surface.get_width()//2, 0))

        self.surface.fill((0,0,0), (self.left.get_rect().right-2, 0, 4, self.surface.get_height()))

    def debuf(self, pos: Vector | tuple[int, int], i: Literal[0, 1]):
        """ Creates a debuf at position `pos` *against* player `i` (on the other player's screen)"""
        c = Collectible(pos, (48, 48), 17, asset.AssetType.ITEM, asset.ItemType.FRUIT, asset.FruitType.PINEAPPLE)
        def l(a, *b, **k):
            if i == 0:
                self.pixel_left += 1
            else:
                self.pixel_right += 1
            
        c.collides_with = l
        return c

    def cherry(self, pos: Vector | tuple[int, int], i: Literal[0, 1]):
        """ Creates a cherry at position `pos` for player `i`"""
        c = Collectible(pos, (48, 48), 17, asset.AssetType.ITEM, asset.ItemType.FRUIT, asset.FruitType.CHERRIES)
        def l(a, *b, **k):
            if i == 0:
                self.pixel_left -= 2
            else:
                self.pixel_right -= 2
            
        c.collides_with = l
        return c
    
    def bananas(self, pos: Vector | tuple[int, int], i: Literal[0, 1]):
        """ Creates a banana at position `pos` for player `i`"""
        c = Collectible(pos, (48, 48), 17, asset.AssetType.ITEM, asset.ItemType.FRUIT, asset.FruitType.BANANAS)
        def l(a, *b, **k): # increase speed
            [self.player1, self.player2][i].speed_mul(1.5, 2)

        c.collides_with = l
        return c

    def spawn(self, i: Literal[0, 1]):
        """ Spawns a collectible around the player indicated by `i`"""

        d_pos = Vector.random_unit_vector() * 64 * 2 * (random() + 1)

        match choice(['cherry', 'banana', 'debuf']):
            case 'cherry':
                if i == 0:
                    self.add_left(self.cherry(self.player1.pos + d_pos, i))
                else:
                    self.add_right(self.cherry(self.player2.pos + d_pos, i))
            case 'banana':
                if i == 0:
                    self.add_left(self.bananas(self.player1.pos + d_pos, i))
                else:
                    self.add_right(self.bananas(self.player2.pos + d_pos, i))
            case 'debuf':
                if i == 0:
                    self.add_left(self.debuf(self.player1.pos + d_pos, 1-i))
                else:
                    self.add_right(self.debuf(self.player2.pos + d_pos, 1-i))

    def check_lose_condition(self):
        # this function is uselessly rigourous or however you spell it

        if self.pixel_left == self.pixel_right:
            return True
        
        if max(self.pixel_left, self.pixel_right) < self.lose_pix_amount:
            return True
        
        self.game_over(1 if self.pixel_left > self.pixel_right else 0)
        return 1
        
    def game_over(self, i: Literal[0, 1]):
        endscreen(self.surface, f"Player {i + 1} wins!")

    def tick(self):
        if self.player1.pos.x - self.camera_position_left.x < self.scroll_tolerance.x: # left
            self.camera_position_left.x = self.player1.pos.x - self.scroll_tolerance.x

        if self.player1.pos.x + self.player1.rect.width - self.camera_position_left.x > self.left.get_width() - self.scroll_tolerance.x:
            self.camera_position_left.x = self.player1.pos.x - self.left.get_width() + self.scroll_tolerance.x + self.player1.rect.width

        if self.player1.pos.y - self.camera_position_left.y < self.scroll_tolerance.y:
            self.camera_position_left.y = self.player1.pos.y - self.scroll_tolerance.y

        if self.player1.pos.y + self.player1.rect.height - self.camera_position_left.y > self.left.get_height() - self.scroll_tolerance.y:
            self.camera_position_left.y = self.player1.pos.y - self.left.get_height() + self.scroll_tolerance.y + self.player1.rect.height
        
        
        if self.player2.pos.x - self.camera_position_right.x < self.scroll_tolerance.x: # left
            self.camera_position_right.x = self.player2.pos.x - self.scroll_tolerance.x

        if self.player2.pos.x + self.player2.rect.width - self.camera_position_right.x > self.left.get_width() - self.scroll_tolerance.x:
            self.camera_position_right.x = self.player2.pos.x - self.left.get_width() + self.scroll_tolerance.x + self.player2.rect.width

        if self.player2.pos.y - self.camera_position_right.y < self.scroll_tolerance.y:
            self.camera_position_right.y = self.player2.pos.y - self.scroll_tolerance.y

        if self.player2.pos.y + self.player2.rect.height - self.camera_position_right.y > self.left.get_height() - self.scroll_tolerance.y:
            self.camera_position_right.y = self.player2.pos.y - self.left.get_height() + self.scroll_tolerance.y + self.player2.rect.height

        if len([i for i in self.left_objects if isinstance(i, Collectible) and abs(self.player1.pos - Vector(*i.rect.center)) < 64 * 5]) == 0:
            self.spawn(0)

        if len([i for i in self.right_objects if isinstance(i, Collectible) and abs(self.player2.pos - Vector(*i.rect.center)) < 64 * 5]) == 0:
            self.spawn(1)

        if self.check_lose_condition() is 1:
            return 1

        self.player1.check_vertical_collision(self.left_objects)
        self.player2.check_vertical_collision(self.right_objects)

        self.pixel_left += self.pixel_rate * (time() - self.prev_pix)
        self.pixel_right += self.pixel_rate * (time() - self.prev_pix)
        self.prev_pix = time()

        self.camera_position = self.camera_position_left
        for obj in self.left_objects:
            obj.tick()

        self.camera_position = self.camera_position_right
        for obj in self.right_objects:
            obj.tick()

class _SfcPartial():
    """Used for the multiple screens on this level, so children can blit"""
    def __init__(self, camera_position: Vector, surface: pygame.Surface) -> None:
        self.camera_position = camera_position
        self.surface = surface
    
    def blit(self, surface: pygame.Surface, pos: Vector | tuple[int, int], rect: pygame.Rect = None):
        """Blits to screen, considering camera position"""
        
        self.surface.blit(surface, tuple(Vector(*pos) - self.camera_position), rect)