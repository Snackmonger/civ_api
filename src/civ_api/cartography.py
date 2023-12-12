
from dataclasses import dataclass
from loguru import logger
from typing import Any, Callable, Optional, TypedDict

from .entities import City, Entity
from .protocols import DoesOccupyCoordinates
from .type_aliasing import Coords

X = 'x'
Y = 'y'


class Tile():
    '''
    A square on a cartesian map.
    '''

    def __init__(
            self,
            uuid: str,
            x: int,
            y: int,
            resources: dict[str, int],
            resource_multiplier: int = 2,
            movement_multiplier: int = 2,
            occupier_uuid: Optional[str] = None,
            is_mountain: bool = False,
            is_water: bool = False
            ) -> None:
        
        self.uuid: str = uuid
        self.x: int = x
        self.y: int = y
        self.resources: dict[str, int] = resources
        self.resource_multiplier: int = resource_multiplier
        self.movement_multiplier: int = movement_multiplier
        self.occupier_uuid: Optional[str] = occupier_uuid
        self.is_mountain: bool = is_mountain
        self.is_water: bool = is_water

    def __repr__(self) -> str:
        return f"Tile {self.uuid} ({self.x}, {self.y}) = {self.resources}"
    
    @property
    def is_occupied(self) -> bool:
        return self.occupier_uuid is not None
    
    @property
    def can_be_occupied(self) -> bool:
        # return find_leaf_uuid(self).can_be_occupied
        return False

    def depart(self, occupier_uuid: str):
        if occupier_uuid == self.occupier_uuid:
            self.occupier_uuid = None

    def arrive(self, occupier_uuid: str) -> None:
        if self.occupier_uuid is None:
            self.occupier_uuid = occupier_uuid

    @property
    def coords(self) -> tuple[int, int]:
        return (self.x, self.y)


class TileDict(TypedDict):
    uuid: str
    x: int
    y: int
    resources: dict[str, int]
    resource_multiplier: int
    movement_multiplier: int
    occupier_uuid: Optional[str]
    is_mountain: bool
    is_water: bool


class Map:
    def __init__(self,
                 width: int,
                 height: int,
                 tiles: dict[str, TileDict] | None = None
                 ) -> None:

        self.width: int = width
        self.height: int = height
        self.tiles: dict[str, TileDict] = tiles or {}
        self.callbacks: dict[str, Callable[..., Any]]


    def tile_is_valid(self, tile: Tile) -> bool:
        if not tile.uuid in self.tiles:
            return not all([tile.x > self.width,
                            tile.y > self.height,
                            tile.x < 0,
                            tile.y < 0])
        return False


    def add_tile(self, tile: TileDict) -> None:
        tile_ = Tile(**tile)
        if self.tile_is_valid(tile_):
            self.tiles.update({tile_.uuid: tile})
            logger.debug(f'Added to map tile with ID: {tile_.uuid}')

        logger.debug('Tile could not be added to map.')


    def get_tile_uuid(self, search: Tile | Coords | Entity | Any) -> str | None:
        '''Find the tile uuid for a given object, if it exists.'''
        if isinstance(search, Tile):
            return search.uuid
        elif isinstance(search, Entity):
            search = search.coords

        if isinstance(search, tuple):
            if len(search) == 2 and all(list(map(lambda x : isinstance(x, int), search))):
                try:
                    self.get_tile_uuid_from_coords(search)
                except ValueError as e:
                    logger.debug(f'Unable to get tile uuid. Error: {e}')
        else:
            logger.debug(f'Unable to get tile uuid: unknown request type [ {search} :: {type(search)} ]')


    
    def get_tile_uuid_from_coords(self, coords: Coords) -> str:
        for uuid, data in self.tiles.items():
            if (data[X], data[Y]) == coords:
                return uuid
        raise ValueError(f'No tile found at coordinates {coords}')
    

    def get_tile_from_coords(self, coords: Coords) -> Tile | None:
        try:
            return self.get_tile_from_uuid(self.get_tile_uuid_from_coords(coords))
        except ValueError as e:
            logger.debug(f'Unable to create tile. Error: {e}')


    def get_tile_from_uuid(self, uuid: str) -> Tile | None:
        if uuid in self.tiles:
            return Tile(**self.tiles[uuid])
        logger.debug(f'No tile found with ID: {uuid}')


    def get_total_resources(self, list_of_coords: list[Coords]) -> dict[str, int]:
        '''
        Get the total resources of all tiles within a city's sphere of influence.
        '''
        # resources: dict[str, int] = {}
        # for tile_ in tiles:
        #     tile = Tile(**self.tiles[tile_])
        #     for resource, amount in tile.resources.items():
        #         before: int = resources.get(resource, 0)
        #         resources[resource] = before + amount
        #     del (tile)
        # return resources
