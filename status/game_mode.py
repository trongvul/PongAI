from enum import Enum, unique


@unique
class GameMode(Enum):
    TWO_PLAYERS = 0
    ONE_PLAYER_EASY = 1
    ONE_PLAYER_DIFFCULT = 2
