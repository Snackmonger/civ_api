from random import choice, randint
from typing import Mapping, Optional
from uuid import uuid4
from loguru import logger

from .entities import City, Entity
from .bases import ProtocolCollator
from .cartography import Map, Tile
from .classes import Coords
from .constants.resources import resource_minmax

ResourceRanges = Mapping[str, tuple[int, int]]

class Abstraction: pass


def test_get_random_resources(resource_ranges: ResourceRanges | None = None
                              ) -> dict[str, int]:
    '''
    Get a random assortment of the given resources.
    '''
    if resource_ranges is None:
        resource_ranges = resource_minmax

    number_of_resources = randint(1, 4)
    resources: dict[str, int] = {}
    for _ in range(number_of_resources):
        res = choice(list(resource_ranges))
        while res in resources:
            res = choice(list(resource_ranges))

        val = choice(resource_ranges[res])
        val = choice(range(1, val + 1))
        resources.update({res:val})

    return resources


def get_neighbouring_tiles(coords: tuple[int, int],
                           map_dimensions: tuple[int, int],
                           depth: int = 1
                           ) -> list[tuple[int, int]]:
    '''
    Return a list of tile objects occupying the neighbouring squares at a
    given depth (diagonal squares count as 1 deep, as the bishop moves).
    '''
    mods: list[int] = [1, -1]
    steps = range(1, depth + 1)
    types_of_x: list[int] = [coords[0] + (mod * step) for mod in mods for step in steps]
    types_of_y: list[int] = [coords[1] + (mod * step) for mod in mods for step in steps]
    types_of_x.append(coords[0])
    types_of_y.append(coords[1])
    coords_: list[tuple[int, int]] = [(x, y) for x in types_of_x for y in types_of_y]

    logger.debug(f'coords_ {len(coords_)}')

    # Any negative x or y must be dropped since the tiles do not exist.
    # TODO: this should also take account of the map max x and max y
    coords_ = list(filter(lambda v : all([v[0] >= 0, 
                                          v[1] >= 0, 
                                          v[0] <= map_dimensions[0],
                                          v[1] <= map_dimensions[1]]),
                                    coords_))
    coords_.remove((coords[0], coords[1]))
    return coords_




def remove_occupier(map_: Map, occupier_uuid: str) -> None:
    ...


def force_relocation(map_: Map, occupier_id: str) -> None:
    ...


def new_city(map_: Map,
             user_uuid: str,
             tile: Tile
             ) -> City:
    
    a = str(uuid4())
    i = str(uuid4())
    city = City(user_uuid, a, i, 4, 30)
    city.population = 5
    city.level = 1
    city.defense = 5
    city.attack = 5
    return city

    
def extract_coordinates(entities: list[Entity]) -> dict[str, tuple[int, int]]:
    '''Return the uuid and coordinates for all entities in a list.'''


def fetch_abstraction(abstract_uuid: str) -> Abstraction:
    '''If the main game object does not already have an abstraction in the 
    list of abstractions, then fetch the data from the database and create
    the abstraction to add to the list.'''

    
    

