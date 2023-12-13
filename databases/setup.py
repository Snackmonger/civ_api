'''Database setup script.'''

import sqlite3
from random import randint, choice
from uuid import uuid4
from loguru import logger


from src.civ_api.constants import Resources
from src.civ_api.functions import vals
from src.civ_api.type_aliasing import (ImmutableType, 
                                       BasicDict, 
                                       ResourceRanges)


TEST_DATABASE = 'databases/test.db'




def setup_database(database_path: str) -> None:
    con: sqlite3.Connection = sqlite3.connect(database_path)
    cur: sqlite3.Cursor = con.cursor()

    user_uuids = """
                CREATE TABLE IF NOT EXISTS users(
                user_uuid TEXT PRIMARY KEY NOT NULL,
                last_updated TEXT,
                current_turn INT,
                current_state TEXT
                );
                """
    
    tiles = """
                CREATE TABLE IF NOT EXISTS tiles
                (
                tile_uuid TEXT PRIMARY KEY NOT NULL,
                user_uuid TEXT NOT NULL,
                x INT NOT NULL, 
                y INT NOT NULL,
                FOREIGN KEY(user_uuid) REFERENCES users(user_uuid)
                );
                """
    
    _res: list[str] = vals(Resources)
    _mod: str = " INT DEFAULT 0, "
    _vals: str = _mod.join(_res) + _mod

    resources = f"""
                CREATE TABLE IF NOT EXISTS resources
                (
                tile_uuid TEXT PRIMARY KEY NOT NULL, 

                {_vals}

                FOREIGN KEY(tile_uuid) REFERENCES tiles(tile_uuid)
                );
                """
    
    abstract_units = """
                CREATE TABLE IF NOT EXISTS abstract_units
                (
                abstract_uuid TEXT PRIMARY KEY NOT NULL,
                unit_name TEXT NOT NULL,
                base_attack_strength INT NOT NULL,
                base_defense_strength INT NOT NULL,
                attack_type TEXT NOT NULL,
                attack_range INT NOT NULL
                );
                """
    
    concrete_units = """
                CREATE TABLE IF NOT EXISTS units
                (
                unit_uuid TEXT PRIMARY KEY NOT NULL,
                abstract_uuid TEXT NOT NULL,
                current_health INT NOT NULL,
                upgrades TEXT,

                FOREIGN KEY(abstract_uuid) REFERENCES abstract_units(abstract_uuid)
                );
                """
    

    setup_tables = [user_uuids, 
                    tiles, 
                    resources, 
                    abstract_units, 
                    concrete_units]
    
    for x in setup_tables:
        logger.debug(f'Creating table with SQL query: {x}')
        cur.execute(x)
    con.commit()


def test_get_random_resources(resource_ranges: ResourceRanges | None = None
                                ) -> BasicDict:
    '''
    Get a random assortment of the given resources.
    '''
    resource_minmax = {'iron': (1, 5),
                        'water': (1, 5),
                        'wheat': (1, 5), 
                        'horses': (1, 5),
                        'sheep': (1, 5),
                        'gems': (1, 5),
                        'olives': (1, 5),
                        'wood': (1, 5)}
    
    if resource_ranges is None:
        resource_ranges = resource_minmax

    number_of_resources = randint(1, 4)
    resources: dict[str, int] = {}
    for _ in range(number_of_resources):
        logger.debug(f'Choosing resource # {_} for collection {resources}')
        res = choice(list(resource_ranges))


        while res in resources:
            logger.debug(f'Resource {res} already selected, trying again...')
            res = choice(list(resource_ranges))

        val = choice(resource_ranges[res])
        val = choice(range(1, val + 1))
        logger.debug(f'Created resource {res}={val}')
        resources.update({res:val})

    # logger.debug(f'Checking full table members for table {resources}')
    # for resource in vals(Resources):
    #     logger.debug(f'Checking {resource}, type{type(resource)}')
    #     if resource not in resources:
    #         logger.debug('Resource not present. Adding now.')
    #         resources.update({resource:0})

    logger.debug(f'Completed resource generation {resources}.')
    return resources



