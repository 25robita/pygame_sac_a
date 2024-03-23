import pygame

from .key_state import KeyState

class KeyListener:
    def __init__(self) -> None:
        self.prev_keys = pygame.key.get_pressed()
        self.keys = pygame.key.get_pressed()

    def tick(self):
        self.prev_keys = self.keys
        self.keys = pygame.key.get_pressed()

    def __getitem__(self, key: int) -> KeyState:
        if self.prev_keys[key]:
            if self.keys[key]:
                return KeyState.KEY_HOLD
            return KeyState.KEY_UP
        if self.keys[key]:
            return KeyState.KEY_DOWN
        return KeyState.NOT_PRESSED