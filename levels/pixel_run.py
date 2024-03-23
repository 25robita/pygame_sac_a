from typing import Literal
from math import sin, cos
from time import time
from json import dump, load

import pygame
from pygame import Surface
from PIL import Image, ImageFilter

from . import LevelManager

import asset
from object import Object
from object.tile_sheet import TileSheet
from object.block import Block
from object.falling_block import FallingBlock
from object.collectible import Collectible
from object.endpoint import Endpoint
from const import DISPLAY_SIZE
from player import Player
from vector import Vector

from endscreen import endscreen
from player_selector import player_selector

class PixelRun(LevelManager):
    def __init__(self, surface: Surface) -> None:
        super().__init__(surface)
        self.prev_pixel = time()
        self.pixel_rate = 0.5
        self.time_start = None

        self.has_won = False

        self.scroll_tolerance = Vector(100, 64)

        self.player_start_point = Vector(100, 100)

        self.score_font = pygame.font.Font(asset.get_asset_path(asset.AssetType.FONT, asset.FontType.SMOKUM), 50)

    def reset(self):
        super().reset()
        self.has_won = False
        self.parent.pixelate = 0

    def add(self, *objs: Object):
        for obj in objs:
            self.objects.append(obj)
            obj.adopt(self)

    def start(self):
        player_type = player_selector(self.surface)

        character_type: asset.CharacterType = [
            asset.CharacterType.MASK_DUDE,
            asset.CharacterType.NINJA_FROG,
            asset.CharacterType.PINK_MAN,
            asset.CharacterType.VIRTUAL_GUY
        ][player_type]

        self.prev_pixel = time()

        self.add(TileSheet((0,0), DISPLAY_SIZE, asset.get_asset_path(asset.AssetType.BACKGROUND, asset.BackgroundType.PURPLE)))
        self.player = Player(self.player_start_point, (48, 48), self.key_listener, character_type)
        self.player.top_down = False
        self.add(self.player)

        if player_type == 0:
            self.player.jump_limit = 1
            self.player.jump_size = 800
            self.player.speed = 400
        elif player_type == 1:
            self.player.jump_size = 800
        elif player_type == 2:
            pass
        elif player_type == 3:
            self.player.jump_size = 400
            self.player.jump_limit = 4
            self.player.speed = 450

        self.time_start = time()


        x = lambda n = 1: n * 64
        y = lambda n = 1: DISPLAY_SIZE[1] - n * 64

        def block(_x: int, _y: int) -> Block:
            b = Block((x(_x), y(_y)), (64, 64))
            self.add(b)
            return b

        def fblock(_x: int, _y: int) -> Block:
            b = FallingBlock((x(_x), y(_y)), (64, 64))
            self.add(b)
            return b
        
        def cherry(_x: int, _y: int) -> Collectible:
            collectible = Collectible((x(_x) + (64 - 48) / 2, y(_y) + (64 - 48) / 2), (48, 48), 17, asset.AssetType.ITEM, asset.ItemType.FRUIT, asset.FruitType.CHERRIES)
            def l(*a, **k):
                self.parent.pixelate -= 2

            collectible.collides_with = l
            self.add(collectible)
            return collectible

        blocks = [
            Block((i, y()), (64, 64)) for i in range(0, DISPLAY_SIZE[0], 64)
        ]
        self.add(*blocks)

        block(8, 2)
        cherry(8, 3)

        block(6, 4)
        block(5, 6)

        block(9, 7)

        block(7, 10)

        block(4, 10)
        block(4, 12)
        # cherry(4, 13)

        block(1, 11)

        fblock(9, 12)


        for i in range(12, 18):
            block(i, 12)

        cherry(14, 13)

        
        for i in range(20, 50):
            fblock(i, 12)

        cherry(30, 13)

        for i in range(55, 75):
            block(i, 12)

        self.endpoint = Endpoint((73 * 64, DISPLAY_SIZE[1] - (13 * 64)), (64, 64))

        self.add(self.endpoint)
        self.endpoint.col_listener = self.win

        
    def win(self):
        self.t = time() - self.time_start

        with open("data.json", 'r+') as f:
            obj = load(f)
            f.seek(0)

            assert 'classic' in obj
            assert 'times' in obj['classic']
            assert isinstance(obj['classic']['times'], list)

            obj['classic']['times'].append(self.t)

            f.truncate()
            dump(obj, f)
            
        self.has_won = True

    def draw(self):
        self.surface.fill((255, 255, 0))
        for object in self.objects:
            object.draw(self)

    def game_over(self) -> Literal[0]:
        endscreen(self.surface, "You were eaten by the corruption...")
        return 0

    def tick(self):

        if self.has_won:
            res_text = f"Time: {self.t:.2f}s"
            with open('data.json') as f:
                if self.t == min(load(f)['classic']['times']):
                    res_text = f"New Highscore: {self.t:.2f}s!"
            
            endscreen(self.surface, res_text)
            return 1

        if self.player.pos.x - self.camera_position.x < self.scroll_tolerance.x: # left
            self.camera_position.x = self.player.pos.x - self.scroll_tolerance.x

        if self.player.pos.x + self.player.rect.width - self.camera_position.x > DISPLAY_SIZE[0] - self.scroll_tolerance.x:
            self.camera_position.x = self.player.pos.x - DISPLAY_SIZE[0] + self.scroll_tolerance.x + self.player.rect.width

        if self.player.pos.y - self.camera_position.y < self.scroll_tolerance.y:
            self.camera_position.y = self.player.pos.y - self.scroll_tolerance.y

        if self.player.pos.y + self.player.rect.height - self.camera_position.y > DISPLAY_SIZE[1] - self.scroll_tolerance.y:
            self.camera_position.y = self.player.pos.y - DISPLAY_SIZE[1] + self.scroll_tolerance.y + self.player.rect.height

        super().tick()
        self.player.check_vertical_collision(self.objects)

        self.parent.pixelate += (time() - self.prev_pixel) * self.pixel_rate
        self.prev_pixel = time()

        if self.parent.pixelate > 12:
            return self.game_over()

        if self.player.pos.y > 1000:
            self.player.velocity *= 0
            self.player.pos = self.player_start_point

    def display_timer(self):
        t = (time() - self.time_start)
        text = self.score_font.render(f"{t // 60 :02.0f}:{int(t % 60) :02.0f}.{100 * t % 100:02.0f}", True, (255, 255, 255))
        
        x = Image.frombytes("RGBA", self.surface.get_size(), pygame.image.tobytes(self.surface, "RGBA"))
        im = pygame.image.frombytes(x.filter(ImageFilter.GaussianBlur(6)).tobytes(), self.surface.get_size(), "RGBA")

        height = 65
        width = 150 if text.get_width() + 20 < 150 else text.get_width() + 20
        left = 0
        top = DISPLAY_SIZE[1] - height

        self.surface.blit(im, (left, top), (left, top, width, height))

        s = Surface((width, height), pygame.SRCALPHA, 32)
        s.fill((0, 0, 0))
        s.set_alpha(100)

        self.surface.blit(s, (left, top))

        self.surface.blit(text, (left + 10, top + (65-text.get_height())/2))

    def post_shader(self):
        self.display_timer()