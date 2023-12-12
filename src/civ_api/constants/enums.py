from enum import StrEnum, auto


class UnitMoveTypes(StrEnum):
    '''
    The types of moves that the computer players are allowed to 
    direct their units to perform.

    A unit will attempt to pursue its directive until:
    - the player orders it to stop
    - the player gives it a new directive
    - the directive can no longer be completed
    '''
    ATTACK = auto()
    DEFEND = auto()
    RETREAT = auto()
    TRAVEL = auto()
    EXPLORE = auto()
    DISBAND = auto()


class DiplomaticStatus(StrEnum):
    ENEMY = auto()
    NEUTRAL = auto()
    ALLY = auto()


class OpponentDispositionTypes(StrEnum):
    '''
    The types of basic strategies the computer players are allowed to
    deploy against each other and the user.
    '''
    AGGRESSIVE = auto() # Goal: Conquer all enemies.
    DEFENSIVE = auto() # Goal: Survive until the clock runs out.
    EXPLORATORY = auto() # Goal: Gather 10 wonders by any means.
    MERCANTILE = auto() # Goal: Acquire 1,000,000 gold.
    CULTURED = auto() # Goal: Build the final cultural building.
    ACADEMIC = auto() # Goal: Build the final science building.


class GamePhases(StrEnum):
    '''
    The phases of the game.
    
    These phases determine which interface methods are responsive to the user.
    '''
    # Mostly, this means that GET and POST are available during the user's 
    # control phase, an error response is available during the computer's
    # control phase, and a specific POST is available during the computer's
    # awaiting continue phase (with some GET to help make an informed decision).

    GAME_IS_NOT_LOADED = auto()
    USER_HAS_CONTROL = auto()
    COMPUTER_HAS_CONTROL = auto()
    COMPUTER_AWAITING_USER_CONTINUE = auto()


class ObjectDataCategories(StrEnum):
    ABSTRACT = auto()
    CONCRETE = auto()


class Resources(StrEnum):
    WHEAT = auto()
    WATER = auto()
    STONE = auto()
    MARBLE = auto()
    IRON = auto()
    COAL = auto()
    GEMS = auto()
    HORSES = auto()
    CATTLE = auto()
    SHEEP = auto()
    FISH = auto()
    PEARLS = auto()
    WILD_GAME = auto()
    SUGAR = auto()
    FARMING = auto()
    SALT = auto()
    GOLD = auto()
    SILVER = auto()
    WOOD = auto()
    CLAY = auto()
    OLIVES = auto()
    GRAPES = auto()
    FRUIT = auto()
    IVORY = auto()
    SILK = auto()
    SPICES = auto()
    DYES = auto()
    INCENSE = auto()


class DatabaseTables(StrEnum):
    USER_UUIDS = auto()
    MAPS = auto()
    TILES = auto()
    RESOURCES = auto()
    ABSTRACT_LOOKUP = auto()
    ABSTRACT_UNITS = auto()