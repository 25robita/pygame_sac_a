from typing import Literal

import pygame
from pygame.locals import *

import object
from vector import Vector
from key_listener import KeyListener

class LevelManager:
    objects: list[object.Object]
    surface: pygame.Surface

    started: bool

    camera_position: Vector

    def __init__(self, surface: pygame.Surface) -> None:
        self.objects: list[object.Object] = []
        """Unordered list of all objects in the scene"""

        self.surface = surface
        self.camera_position = Vector(0, 0)
        """Allows for offset of viewpoint"""

        self.started = False

        self.parent = None
        """Parent GameManager"""

        self.key_listener: KeyListener = None

    def reset(self):
        self.started = False
        self.camera_position = Vector(0, 0)
        self.objects = []

    def emancipate(self, obj: object.Object):
        """Remove a child object from scene"""
        self.objects.remove(obj)

    def start(self) -> None:
        """Used to add objects to a scene"""
        self.started = True

    def blit(self, surface: pygame.Surface, pos: Vector | tuple[int, int], rect: pygame.Rect = None):
        """Blits to screen, considering camera position"""
        
        self.surface.blit(surface, tuple(Vector(*pos) - self.camera_position), rect)
    
    def tick(self):
        for object in self.objects:
            object.tick()
    
    def draw(self):
        """Draws the scene. Must be implemented on every class that inherits LevelManager"""
        raise NotImplementedError()

    def loop(self) -> Literal[True, False, 1]:
        for event in pygame.event.get():
            if event.type == QUIT:
                return False
            
        # Processing
        t = self.tick()
        if t is 1:
            return 1
        if t is 0:
            return 0
            
        # Drawing
        self.draw()
            
        # Updating
        # pygame.display.update()

        return True
    
    def post_shader(self):
        """Generally used for UI display"""
        pass