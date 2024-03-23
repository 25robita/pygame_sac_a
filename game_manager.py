from time import time

import pygame
from pygame.locals import *
from pygame import Surface

import asset
from levels import LevelManager
from key_listener import KeyListener
from const import DISPLAY_SIZE
from menu import Menu

class GameManager:
    levels: list[LevelManager]
    key_listener: KeyListener
    surface: Surface

    level_index: int | None

    run_menu: bool


    def __init__(self) -> None:
        pygame.init()
        self.surface = pygame.display.set_mode(DISPLAY_SIZE)
        """Window"""

        pygame.display.set_caption("Pixel Run")
        pygame.display.set_icon(pygame.image.load(asset.get_asset_path(asset.AssetType.ICON)).convert_alpha())

        self.key_listener = KeyListener()
        """Allows for easy detection of key down, up and hold events"""

        self.levels = []
        """Array of levels"""

        self.level_index = None
        """Index of current level"""

        self.pixelate = 0
        """0 for no pixelation, else pixelation factor"""

        self.menu = Menu(self.surface)
        self.run_menu = True

    @property
    def current_level(self) -> LevelManager:
        return self.levels[self.level_index]
    
    def add_level(self, level: LevelManager):
        self.levels.append(level)
        level.key_listener = self.key_listener
        level.parent = self
        if self.level_index is None:
            self.level_index = 0
    
    def main(self) -> None:
        self.loop()
        # handle level changes

        pygame.quit()

    def apply_shader(self):
        if self.pixelate < 2:
            return

        s = pygame.transform.scale(pygame.transform.scale_by(self.surface, 1 / int(self.pixelate)), self.surface.get_size())
        self.surface.blit(s, (0, 0))

    def loop(self) -> None:
        if self.run_menu:
            if not self.menu.started:
                self.menu.start()
            while (res := self.menu.loop()) is True:
                pygame.display.update()
            if res is False:
                return
            self.level_index = res

        if not self.current_level.started:
            self.current_level.start()
        while (res := self.current_level.loop()) is True:
            self.key_listener.tick()
            self.apply_shader()
            self.current_level.post_shader()
            pygame.display.update()

        if res is False:
            return
        self.current_level.reset()
        self.run_menu = True
        self.menu.start()
        self.loop()
        