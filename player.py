from typing import Literal
from time import time
from os import listdir
from os.path import join
from enum import StrEnum

import pygame
from pygame.locals import *

from vector import Vector
from const import *
# from player_type import PlayerType
from object import Object
from object.colliding_object import CollidingObject
from object.collectible import Collectible
from key_listener import KeyListener, KeyState
import asset

class Direction(StrEnum):
    LEFT = "left"
    RIGHT = "right"

    def __mul__(self, other: float) -> float:
        return other * -1 if self == Direction.LEFT else 1

class Player(Object):
    def __init__(self, pos: Vector | tuple[int, int], size: Vector | tuple[int, int], key_listener: KeyListener, character_type: asset.CharacterType = asset.CharacterType.PINK_MAN) -> None:
        super().__init__(pos, size)

        # self.rect = pygame.Rect(x, y, width, height)

        self.velocity = Vector(0, 0)
        self.pos = Vector(*pos)
        self.mass = None

        self.speed = 350 # default values
        self.speed_factor = 1
        self.speed_end: None = None
        self.jump_size = 600 # default values

        self.direction: Direction = Direction.LEFT
        self.animation_count = 0
        self.fall_start = time()

        self.anim_frame = time()
        self.ANIM_DELAY = 0.08

        self.top_down = False

        self.character_type = character_type
        self.sprites: dict[asset.CharacterVariant, dict[Direction, list[pygame.Surface]]] = {}
        self.sprite = pygame.image.load(asset.get_asset_path(asset.AssetType.CHARACTER, self.character_type, asset.CharacterVariant.FALL)).convert_alpha()

        self.listener = key_listener

        self.load_sprites()
        self.update_sprite()

        self.jump_count = 0

        self.prev_move = time()

        self.prev_grav = time()

        self.left_key = pygame.K_LEFT
        self.right_key = pygame.K_RIGHT
        self.up_key = pygame.K_UP
        self.down_key = pygame.K_DOWN
        self.jump_key = pygame.K_SPACE

    def jump(self):
        if self.jump_count >= 2:
            return
        self.velocity.y = -1 * self.jump_size
        self.animation_count = 0
        self.jump_count += 1
        self.fall_start = time()

    def move(self, dx: float, dy: float):
        self.pos += Vector(dx, dy) * (time() - self.prev_move)
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y
        self.prev_move = time()

    def move_left(self, velocity: float):
        self.velocity.x = -velocity
        if self.direction != Direction.LEFT:
            self.direction = Direction.LEFT
            self.animation_count = 0

    def move_right(self, velocity: float):
        self.velocity.x = velocity
        if self.direction != Direction.RIGHT:
            self.direction = Direction.RIGHT
            self.animation_count = 0

    def move_up(self, velocity: float):
        self.velocity.y = -velocity

    def move_down(self, velocity: float):
        self.velocity.y = velocity

    def handle_move(self, objects: list[Object]):
        col_objects = [obj for obj in objects if isinstance(obj, CollidingObject) and obj is not self and obj.physics]

        col_right = self.check_movement_collision(col_objects, self.speed * self.speed_factor * 4)
        col_left = self.check_movement_collision(col_objects, -self.speed * self.speed_factor * 4)

        if self.listener[self.right_key] and not col_right:
            self.move_right(self.speed * self.speed_factor)
        elif self.listener[self.left_key] and not col_left:
            self.move_left(self.speed * self.speed_factor)
        else:
            self.velocity.x = 0

        if self.top_down:
            col_up = self.check_movement_collision(col_objects, 0, -self.speed * self.speed_factor * 4)
            col_down = self.check_movement_collision(col_objects, 0, self.speed * self.speed_factor * 4)
            if self.listener[self.up_key] and not col_up:
                self.move_up(self.speed * self.speed_factor)
            elif self.listener[self.down_key] and not col_down:
                self.move_down(self.speed * self.speed_factor)
            else:
                self.velocity.y = 0

            if self.velocity.x != 0 and self.velocity.y != 0:
                self.velocity.x = self.velocity.x * 0.707
                self.velocity.y = self.velocity.y * 0.707
        

        if not self.top_down and self.listener[self.jump_key] == KeyState.KEY_DOWN:
            self.jump()

    def update_sprite(self):
        # pass
        # name = "idle"

        variant = asset.CharacterVariant.IDLE

        if not self.top_down:
        
            if self.velocity.y < 0:
                if self.jump_count == 1:
                    variant = asset.CharacterVariant.JUMP
                elif self.jump_count == 2:
                    variant = asset.CharacterVariant.DOUBLE_JUMP
            # elif self.velocity.y > GRAVITY * 2:
            #     name = "fall"
            elif self.velocity.x != 0:
                variant = asset.CharacterVariant.RUN

        elif abs(self.velocity) > 0:
            variant = asset.CharacterVariant.RUN

        current_anim = self.sprites[variant][self.direction]

        if time() > self.anim_frame + self.ANIM_DELAY:
            self.animation_count += 1
            self.anim_frame = time()

        self.animation_count %= len(current_anim)
        self.sprite = current_anim[self.animation_count]

    def land(self):
        if self.velocity > 0:
            self.velocity.y = 0
        
        self.jump_count = 0
        self.fall_start = time()

    def hit_head(self):
        self.velocity.y *= -1
        self.fall_start = time()

    def collides_with(self, obj: Object):
        if isinstance(obj, Collectible):
            obj.parent.emancipate(obj)

    def check_vertical_collision(self, objs: list[Object]) -> list[Object]:
        for obj in objs:
            if obj is self:
                continue

            if not isinstance(obj, CollidingObject):
                continue

            if pygame.sprite.collide_mask(self, obj):
                if obj.physics and self.velocity.y > 0:
                    self.rect.bottom = obj.rect.top
                    self.pos.y = self.rect.y
                    self.land()
                elif obj.physics and self.velocity.y < 0:
                    self.rect.top = obj.rect.bottom
                    self.hit_head()
                self.collides_with(obj)
                obj.collides_with(self)

    def check_movement_collision(self, objs: list[Object], dx: int = 0, dy: int = 0) -> None | Object:
        original = (self.rect.x, self.rect.y)
        
        self.rect.x += dx * (time() - self.prev_move)
        self.rect.y += dy * (time() - self.prev_move)
        self.update()
        
        col = None
        
        for obj in objs:
            if pygame.sprite.collide_mask(self, obj):
                col = obj
                break 
        
        self.rect.x, self.rect.y = original
        self.update()
        return col

    def tick(self, objects: list[Object] = None):
        if self.speed_end is not None and self.speed_end <= time():
            self.speed_factor = 1
            self.speed_end = None


        if objects is None:
            objects = self.parent.objects if self.parent is not None else []

        if not self.top_down:
            self.velocity.y += (time() - self.prev_grav) * 1000
            self.prev_grav = time()
        
        self.handle_move(objects)

        self.move(*self.velocity)

        self.update_sprite()
        self.update()

    def update(self):
        self.rect = self.sprite.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.sprite)

    def speed_mul(self, amount: float, duration: float) -> None:
        self.speed_factor = amount
        self.speed_end = duration + time()

    def draw(self, surface: pygame.Surface, offset_x: int = 0, offset_y: int = 0):
        # pygame.draw.rect(surface, "red", self.rect)
        surface.blit(self.sprite, (int(self.rect.x - offset_x), int(self.rect.y - offset_y)))

    def load_sprites(self):
        t = self.character_type

        for variant in asset.CharacterVariant:
            path = asset.get_asset_path(asset.AssetType.CHARACTER, t, variant)

            self.sprites[variant] = {
                Direction.LEFT: [],
                Direction.RIGHT: []
            }

            sheet = pygame.image.load(path).convert_alpha()

            for i in range(sheet.get_width() // 32):
                s = pygame.Surface((32, 32), SRCALPHA, 32)
                s.blit(sheet, (0,0), pygame.Rect(32 * i, 0, 32, 32))
                s = pygame.transform.scale(s, tuple(self.size))
                self.sprites[variant][Direction.RIGHT].append(s)
                self.sprites[variant][Direction.LEFT].append(pygame.transform.flip(s,1,0))