from typing import Literal
from json import load

import pygame
from PIL import Image

import asset
from object.tile_sheet import TileSheet

class Menu:
    def __init__(self, surface: pygame.Surface) -> None:
        self.background: TileSheet | None = None
        self.started = False

        self.surface = surface

        self.button_font = pygame.font.Font(asset.get_asset_path(asset.AssetType.FONT, asset.FontType.REPRISE), 72)

        
    def start(self):
        self.started = True
        self.background = TileSheet((0,0), self.surface.get_size(), asset.get_asset_path(asset.AssetType.BACKGROUND, asset.BackgroundType.BROWN))

        self.title = pygame.image.load(asset.get_asset_path(asset.AssetType.TITLE)).convert_alpha()


        self.button1: list[tuple[pygame.Surface, tuple[int, int]]] = [
            (self.button_font.render("1.", True, (108, 72, 33)), (90, 300)),
            (self.button_font.render("Classic", True, (108, 72, 33)), (170, 300)),
        ]

        self.button2: list[tuple[pygame.Surface, tuple[int, int]]] = [
            (self.button_font.render("2.", True, (108, 72, 33)), (90, 400)),
            (self.button_font.render("Battle", True, (108, 72, 33)), (170, 400)),
        ]

        self.rect1 = pygame.Rect(90, 300, 300, 72)
        self.rect2 = pygame.Rect(90, 400, 300, 72)

        with open('data.json') as f:
            highscore = min(load(f)['classic']['times'])

        
        hs_text = pygame.transform.scale_by(self.button_font.render(
            f"{highscore//60:02.0f}:{int(highscore%60):02.0f}.{100 * highscore % 100:02.0f}",
            True,
            (108, 72, 33)
        ), 0.5)


        self.button1.append((hs_text, (self.surface.get_width() - hs_text.get_width() - 10, 300 + self.button1[0][0].get_height() - hs_text.get_height())))

    def loop(self) -> Literal[True, False, 0, 1]:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.rect1.collidepoint(pygame.mouse.get_pos()):
                    return 0
                if self.rect2.collidepoint(pygame.mouse.get_pos()):
                    return 1
            
        self.draw()

        return True

    def draw(self):
        self.background.draw(self.surface)
        self.surface.blit(self.title, (0, 0))

        pygame.mouse.set_cursor(pygame.cursors.arrow)

        for el, pos in self.button1:
            el.set_alpha(255)
            hov = self.rect1.collidepoint(pygame.mouse.get_pos())
            if hov:
                el.set_alpha(190)

                pygame.mouse.set_cursor(pygame.cursors.ball)

            self.surface.blit(el, pos)

        for el, pos in self.button2:
            el.set_alpha(255)
            hov = self.rect2.collidepoint(pygame.mouse.get_pos())
            if hov:
                el.set_alpha(190)
            
                pygame.mouse.set_cursor(pygame.cursors.ball)

            self.surface.blit(el, pos)
