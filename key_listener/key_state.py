from enum import Enum

class KeyState(Enum):
    KEY_DOWN = 1
    KEY_HOLD = 2
    KEY_UP = 0
    NOT_PRESSED = -1

    def __bool__(self) -> bool:
        return self == KeyState.KEY_DOWN or self == KeyState.KEY_HOLD
