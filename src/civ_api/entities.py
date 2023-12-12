from typing import Optional, Callable



from .bases import ProtocolCollator
from .cartography import Tile
from .classes import Move
from .constants.enums import ObjectDataCategories
from .engine import Abstraction
from .protocols import DoesOccupyCoordinates, DoesJoinBattle


class Entity:
    '''
    An entity is that which occupies a tile.

    Some entities:
    - Spearman
    - River
    - Mountain
    - City
    - Merchant
    - Factory

    An entity might be mobile or immobile. An immobile entity is a fixed feature, unless
    it be removed/destroyed under certain circumstances.

    A tile normally allows one entity to occupy it at a time. However, an
    entity can sometimes occupy another entity, which occupies a tile. 

    Some entities that occupy other entities:
    - A mountain blocks all movement, but a mountain pass allows one unit at a time to occupy it.
    - Several soldiers can occupy a tank, which can then move as a single unit.
    '''

    def __init__(self,
                 abstract_uuid: str,
                 instance_uuid: str,
                 x: int,
                 y: int
                 ) -> None:
        self.abstract_uuid: str = abstract_uuid
        self.instance_uuid: str = instance_uuid
        self.x: int = x
        self.y: int = y
        self.can_be_occupied: bool
        self.is_occupied: bool
        self.callbacks: dict[str, Callable[..., Any]]

    @property
    def abstraction(self) -> Abstraction:
        return self.callbacks[ObjectDataCategories.ABSTRACT](self.abstract_uuid)

    @property
    def block(self) -> bool:
        return any([self.is_occupied, not self.can_be_occupied])
    
    @property
    def is_leaf(self) -> bool:
        return not self.can_be_occupied

    @property
    def coords(self) -> tuple[int, int]:
        return (self.x, self.y)


class Unit(Entity):

    def __init__(self, 
                 empire_uuid: str,
                 abstract_uuid: str,
                 instance_uuid: str,
                 x: int,
                 y: int
                 ) -> None:
        super().__init__(abstract_uuid, instance_uuid, x, y)
        self.empire_uuid: str = empire_uuid
        self.move: Optional[Move]
        self.unit_upgrades: Optional[list[str]]



class City(Entity):

    def __init__(self, 
                 empire_uuid: str,
                 abstract_uuid: str,
                 instance_uuid: str,
                 x: int,
                 y: int
                 ) -> None:
        super().__init__(abstract_uuid, instance_uuid, x, y)
        self.empire_uuid = empire_uuid
        self.city_uuid: str
        self.name: str
        self.population: int
        self.level: int
        self.defense: int
        self.attack: int
        self.units: list[str] = []
        self.tiles: list[str] = []
        self.upgrades: Optional[list[str]] = []


    def end_turn(self) -> None:
        ...

    @property
    def culture_per_turn(self) -> int:
        ...

    @property
    def science_per_turn(self) -> int:
        ...

    @property
    def time_to_expand(self) -> bool:
        '''Flag indicating that the city has met expansion conditions.'''

    def remove_tile(self, tile_uuid: str) -> None:
        if tile_uuid in self.tiles:
            self.tiles.remove(tile_uuid)
        
    def add_tile(self, tile_uuid: str) -> None:
        if tile_uuid not in self.tiles:
            self.tiles.append(tile_uuid)

    @property
    def coords(self) -> tuple[int, int]:
        return (self.x, self.y)
