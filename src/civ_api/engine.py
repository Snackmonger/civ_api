'''Main game object.'''

from uuid import uuid4
from typing import Any, Protocol

from databases.setup import DatabaseManager

from . import events
from .cartography import Tile
from .classes import DiplomaticRelations
from .constants.enums import GamePhases, DiplomaticStatus
from .entities import Unit, City
from .functions import get_neighbouring_tiles
from .type_aliasing import ImmutableType, BasicDict


class UserOrder:
    ...


class Response:
    ...


class Abstraction:
    ...


class DatabaseStrategy():

    def __init__(self, master: 'Game') -> None:
        self.user_uuid: str = master.user_uuid
        self.database_manager: DatabaseManager
    

    def set_user(self, user_uuid: str) -> None:
        self.user_uuid = user_uuid
    

    def update(self, table_name: str, table_dictionary: BasicDict) -> None:
        # self.database_manager...
        ...
    
    def get(self, table_name: str, table_key: str) -> dict[str, ImmutableType]:
        raise NotImplementedError
    
    def make_tile(self, tile_uuid: str) -> Tile:
        ...

    def make_city(self, city_uuid: str) -> City:
        ...

    def make_unit(self, unit_uuid: str) -> Unit:
        ...


class Empire:
    '''Container for player-related data.'''

    def __init__(self) -> None:
        self.name: str
        self.description: str
        self.diplomatic_relations: DiplomaticRelations
        self.cities: list[City]
        self.units: list[Unit]

    def get_city(self, city_uuid: str) -> City:
        for city in self.cities:
            if city_uuid == city.city_uuid:
                return city
            
        # city_data = db.get(???)

    @property
    def science_per_turn(self) -> int:
        ...

    @property
    def culture_per_turn(self) -> int:
        ...

    def turn(self):
        ...


class Game:

    def __init__(self, user_uuid: str, database: DatabaseStrategy) -> None:
        self.user_uuid: str = user_uuid
        self.database: DatabaseStrategy = database
        self.database.set_user(user_uuid)

        self.current_phase: GamePhases # = self.database.get_phase(user_uuid)
        self.abstractions: list[Abstraction] # = self.database.fetch_abstractions()
        self.empires: list[Empire] # = self.database.get_empires(user_uuid)
        self.visible_tiles: list[Tile] # = self.database.get_tiles(user_uuid)


    



    def user_continue(self) : # -> dict[str, str]:
        '''
        When the game is in the COMPUTER AWAITING USER CONTINUE phase, it 
        returns a prompt with every API call reminding the user that the end-of-turn
        results cannot finish processing until the user responds to the prompt.
        
        As the user responds to one prompt, the next one is queued and returned with the
        response from the first. Once all prompts are dealt with, the final prompt returns
        a response containing the final end-of-turn report. 
        
                                                            (the end of turn report should
        also be saved to the database, so that we can fetch it if the user wants a reminder
        of what happened the last time the game was being played.)
        '''


    def user_order(self, order: UserOrder) -> Response:
        ...
        if not self.current_phase == GamePhases.USER_HAS_CONTROL:
            ...


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


    





