from typing import TYPE_CHECKING, Protocol
from .events import Event


if TYPE_CHECKING:
    from .cartography import Tile
    from typing import Any


class DoesOccupyCoordinates(Protocol):

    @property
    def coords(self) -> tuple[int, int]:
        '''Return a tuple (x, y)'''
        raise NotImplementedError
    
    @property
    def tile(self) -> 'Tile':
        '''Return the tile being occupied.'''
        raise NotImplementedError
    

class CanBeOccupied(Protocol):

    def add_occupier(self, occupier: DoesOccupyCoordinates) -> None:
        raise NotImplementedError
    
    def remove_occupier(self, occupier: DoesOccupyCoordinates) -> None:
        raise NotImplementedError
    
    @property
    def is_occupied(self) -> bool:
        raise NotImplementedError



class DoesJoinBattle(Protocol):

    def attack(self, defender: 'DoesJoinBattle') -> None:
        '''Post an event requesting a calculation of the attack.'''
        raise NotImplementedError

    def defend(self) -> None:
        '''Post an event requesting that a defender bonus be applied to this unit.'''
        raise NotImplementedError
    


class DoesHandleCallbacks(Protocol):
    
    def handle(self, event: Event) -> None:
        '''Catch an event and forward the data to the appropriate method.'''
        raise NotImplementedError