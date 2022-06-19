from enum import Enum, unique


@unique
class GameState(Enum):
    MENU = 0
    SERVE = 1
    PLAY = 2
    END = 3
