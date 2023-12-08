'''Main game object.'''

from uuid import uuid4
from typing import Any

from . import events
from .cartography import Tile
from .classes import DiplomaticRelations
from .constants.enums import GamePhases, DiplomaticStatus
from .entities import Unit, City
from .functions import get_neighbouring_tiles

class UserOrder:
    ...

class Response:
    ...

class Abstraction:
    ...

class DatabaseStrategy:
    ...

class Empire:
    ...

    def __init__(self) -> None:
        self.name: str
        self.description: str

    def turn(self):
        ...


class User:
    ...


class Game:

    def __init__(self) -> None:
        self.user_uuid: str
        self.current_phase: GamePhases
        self.database: DatabaseStrategy

        self.abstractions: list[Abstraction] # = self.database.fetch_abstractions()
        self.empires: list[Empire] = []
        self.diplomacy: DiplomaticRelations

        # Populate list of entity uuid from database
        self.tiles: list[str] = []
        self.cities: list[str] = []
        self.units: list[str] = []

        self.must_resolve: list[Any]
        # we need a place to store decision-based forks that must be resolved
        # by the user before the next turn can begin. for instance, if the 
        # user defeats a city, the user must decide whether to occupy, destroy,
        # plunder the city before being able to move to the next turn.


    def user_order(self, order: UserOrder) -> Response:
        ...
        if not self.current_phase == GamePhases.USER_HAS_CONTROL:
            ...
            # self.defer(order)


    # def new(self):
    #     new_map_w = 10
    #     new_map_h = 10
        
    #     for x in range(new_map_w):
    #         for y in range(new_map_h):
    #             uuid = str(uuid4())
    #             resources = get_random_resources()
    #             self.tiles.append(Tile(uuid, x, y, resources))

    #     tile: Tile 
    #     tiles: list[Tile] = []
    #     for tile in self.tiles:
    #         if (tile.x, tile.y) == (5, 5):
    #             tiles = get_neighbouring_tiles(self.tiles, tile, 2)

    #     for tile_ in tiles:
    #         print(tile_)



    def end_turn(self) -> None:
        self.current_phase = GamePhases.COMPUTER_HAS_CONTROL
        # the game needs to be able to pause in the calculation of the 
        # computer player moves in case it needs to receive input from
        # the player to continue.
        for player in self.empires:
            player.turn()



    def move_unit(self, unit_uuid: str, coords: tuple[int, int]) -> None:

        # check whether the coords are within range
        # check whether the coords can be occupied
        # if hostile entity on coords, user must use 'attack' method
        ...


    def attack(self, unit_uuid: str, coords: tuple[int, int]) -> None:
        ...


    





