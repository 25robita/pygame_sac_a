from os.path import join
from enum import StrEnum
from typing import Literal

import pygame

from const import ASSETS_DIR

class AssetType(StrEnum):
    BACKGROUND = "Background"
    ITEM = "Items"
    CHARACTER = "MainCharacters"
    MENU = "Menu"
    TERRAIN = "Terrain"
    TRAPS = "Traps"
    FONT = "Font"
    OTHER = "Other"
    TITLE = "title.png"
    ICON = "icon.png"

class BackgroundType(StrEnum):
    BLUE = "Blue.png"
    BROWN = "Brown.png"
    GRAY = "Gray.png"
    GREEN = "Green.png"
    PINK = "Pink.png"
    PURPLE = "Purple.png"
    YELLOW = "Yellow.png"

class ItemType(StrEnum):
    BOX = "Boxes"
    CHECKPOINT = "Checkpoints"
    FRUIT = "Fruits"

class BoxType(StrEnum):
    BOX_1 = "Box1"
    BOX_2 = "Box2"
    BOX_3 = "Box3"

class BoxVariant(StrEnum):
    BREAK = "Break.png"
    HIT = "Hit (28x24).png"
    IDLE = "Idle"

class CheckpointType(StrEnum):
    CHECKPOINT = "Checkpoint"
    END = "End"
    START = "Start"

class Checkpoint_CheckpointVariant(StrEnum):
    FLAG_IDLE = "Checkpoint (Flag Idle)(64x64).png"
    FLAG_OUT = "Checkpoint (Flag Out)(64x64).png"
    NO_FLAG = "Checkpoint (No Flag).png"

class Checkpoint_EndVariant(StrEnum):
    IDLE = "End (Idle).png"
    PRESSED = "End (Pressed).png"

class Checkpoint_StartVariant(StrEnum):
    IDLE = "Start (Idle).png"
    MOVING = "Start (Moving) (64x64).png"

class FruitType(StrEnum):
    APPLE = "Apple.png"
    BANANAS = "Bananas.png"
    CHERRIES = "Cherries.png"
    KIWI = "Kiwi.png"
    MELON = "Melon.png"
    ORANGE = "Orange.png"
    PINEAPPLE = "Pineapple.png"
    STRAWBERRY = "Strawberry.png"
    COLLECTED = "Collected.png"

class CharacterType(StrEnum):
    MASK_DUDE = "MaskDude"
    NINJA_FROG = "NinjaFrog"
    PINK_MAN = "PinkMan"
    VIRTUAL_GUY = "VirtualGuy"

class CharacterVariant(StrEnum):
    JUMP = "jump.png"
    DOUBLE_JUMP = "double_jump.png"
    WALL_JUMP = "wall_jump.png"
    FALL = "fall.png"
    HIT = "hit.png"
    IDLE = "idle.png"
    RUN = "run.png"

CHARACTER_APPEARING = "Appearing (96x96).png"
CHARACTER_DISAPPEARING = "Desappearing (96x96).png"

class MenuType(StrEnum):
    BUTTON = "Buttons"
    LEVEL = "Level"
    TEXT = "Text"

class ButtonType(StrEnum):
    ACHIEVEMENTS = "Achievements.png"
    BACK = "Back.png"
    CLOSE = "Close.png"
    LEADERBOARD = "Leaderboard.png"
    LEVELS = "Levels.png"
    NEXT = "Next.png"
    PLAY = "Play.png"
    PREVIOUS = "Previous.png"
    RESTART = "Restart.png"
    SETTINGS = "Settings.png"
    VOLUME = "Volume.png"

class Level:
    def __getitem__(self, i: int) -> str:
        assert 0 < i <= 50
        return f"{i:02}.png"

class TextType(StrEnum):
    BLACK = "Text (Black) (8x10).png"
    WHITE = "Text (White) (8x10).png"

TERRAIN = "Terrain.png"

class TrapType(StrEnum):
    ARROW = "Arrow"
    BLOCK = "Blocks"
    FALLING_PLATFORM = "Falling Platforms"
    FAN = "Fan"
    FIRE = "Fire"
    PLATFORM = "Platforms"
    ROCK_HEAD = "Rock Head"
    SAND_MUD_ICE = "Sand Mud Ice"
    SAW = "Saw"
    SPIKE_HEAD = "Spike Head"
    SPIKED_BALL = "Spiked Ball"
    SPIKES = "Spikes"
    TRAMPOLINE = "Trampoline"

class ArrowVariant(StrEnum):
    HIT = "Hit (18x18).png"
    IDLE = "Idle (18x18).png"

class BlockVariant(StrEnum):
    HIT_SIDE = "HitSide (22x22).png"
    HIT_TOP = "HitTop (22x22).png"
    IDLE = "Idle.png"
    PART_1 = "Part 1 (22x22).png"
    PART_2 = "Part 2 (22x22).png"

class FallingPlatformVariant(StrEnum):
    OFF = "Off.png"
    ON = "On (32x10).png"

class FanVariant(StrEnum):
    OFF = "Off.png"
    ON = "On (24x8).png"

class FireVariant(StrEnum):
    HIT = "hit.png"
    OFF = "off.png"
    ON = "on.png"

class PlatformVariant(StrEnum):
    BROWN_OFF = "Brown Off.png"
    BROWN_ON = "Brown On (32x8).png"
    CHAIN = "Chain.png"
    GREY_OFF = "Grey Off.png"
    GREY_ON = "Grey On (32x8).png"

class RockHeadVariant(StrEnum):
    BLINK = "Blink (42x42).png"
    IDLE = "Idle.png"
    HIT_BOTTOM = "Bottom Hit (42x42).png"
    HIT_TOP = "Top Hit (42x42).png"
    HIT_LEFT = "Left Hit (42x42).png"
    HIT_RIGHT = "Right Hit (42x42).png"

class SandMudIceVariant(StrEnum):
    ICE_PARTICLE = "ICE Particle.png"
    MUD_PARTICLE = "Mud Particle.png"
    SAND_PARTICLE = "Sand Particle.png"
    SAND_MUD_ICE = "Sand Mud Ice (16x6).png"

class SawVariant(StrEnum):
    CHAIN = "Chain.png"
    OFF = "off.png"
    ON = "on.png"

class SpikeHeadVariant(StrEnum):
    BLINK = "Blink (54x52).png"
    IDLE = "Idle.png"
    HIT_BOTTOM = "Bottom Hit (54x52).png"
    HIT_TOP = "Top Hit (54x52).png"
    HIT_LEFT = "Left Hit (54x52).png"
    HIT_RIGHT = "Right Hit (54x52).png"

class SpikedBallVariant(StrEnum):
    CHAIN = "Chain.png"
    SPIKED_BALL = "Spiked Ball.png"

class SpikesVariant(StrEnum):
    IDLE = "Idle.png"

class TrampolineVariant(StrEnum):
    IDLE = "Idle.png"
    JUMP = "Jump (28x28).png"

class FontType(StrEnum):
    SMOKUM = join("Smokum", "Smokum-Regular.ttf")
    VT323 = join("VT323", "VT323-Regular.ttf")
    REPRISE = "RepriseTitleStd.otf"

def get_asset_path(type: AssetType, *specifiers:  BackgroundType | ItemType | BoxType | BoxVariant | CheckpointType | Checkpoint_CheckpointVariant | Checkpoint_EndVariant | Checkpoint_StartVariant | FruitType | CharacterType | CharacterVariant | MenuType | ButtonType | TextType | TrapType | ArrowVariant | BlockVariant | FallingPlatformVariant | FanVariant | FireVariant | PlatformVariant | RockHeadVariant | SandMudIceVariant | SawVariant | SpikeHeadVariant | SpikedBallVariant | SpikesVariant | TrampolineVariant | str):
    return join(ASSETS_DIR, type, *specifiers)


def select(sprite_sheet: pygame.Surface, sprite_size: tuple[int, int], index: tuple[int, int], destination: pygame.Surface | None = None) -> pygame.Surface | None:
    if destination is None:
        destination = pygame.Surface(sprite_size, pygame.SRCALPHA, 32)

    
