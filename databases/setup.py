'''Database setup script.'''

import sqlite3
from random import randint, choice
from uuid import uuid4
from loguru import logger

from src.civ_api.constants import Resources, vals
from src.civ_api.type_aliasing import ImmutableType, SQLTableDict, ResourceRanges

TEST_DATABASE = 'databases/test.db'




def setup_database(database_path: str) -> None:
    con: sqlite3.Connection = sqlite3.connect(database_path)
    cur: sqlite3.Cursor = con.cursor()

    user_uuids = 'CREATE TABLE IF NOT EXISTS user_uuids(user_uuid TEXT PRIMARY KEY NOT NULL);'

    maps = """
                CREATE TABLE IF NOT EXISTS maps
                (
                map_uuid TEXT PRIMARY KEY NOT NULL, 

                user_uuid TEXT NOT NULL,
                last_updated TEXT,
                current_turn INT,
                current_state TEXT,

                FOREIGN KEY(user_uuid) REFERENCES user_uuids(user_uuid)
                );
                """
    
    tiles = """
                CREATE TABLE IF NOT EXISTS tiles
                (
                tile_uuid TEXT PRIMARY KEY NOT NULL,
                map_uuid TEXT NOT NULL,
                x INT NOT NULL, 
                y INT NOT NULL,
                FOREIGN KEY(map_uuid) REFERENCES maps(map_uuid)
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
    
    abstraction_types = """
                CREATE TABLE IF NOT EXISTS abstract_lookup
                (
                abstract_uuid TEXT PRIMARY KEY NOT NULL,
                abstract_category TEXT NOT NULL
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
                attack_range INT NOT NULL,

                FOREIGN KEY(abstract_uuid) REFERENCES abstract_lookup(abstract_uuid)
                );
                """
    
    concrete_units = """
                CREATE TABLE IF NOT EXISTS abstract_units
                (
                unit_uuid TEXT PRIMARY KEY NOT NULL,
                abstract_uuid TEXT NOT NULL,
                current_health INT NOT NULL,
                upgrades TEXT,

                FOREIGN KEY(abstract_uuid) REFERENCES abstract_units(abstract_uuid)
                );
                """
    

    setup_tables = [user_uuids, maps, tiles, resources, abstraction_types, abstract_units, concrete_units]
    for x in setup_tables:
        logger.debug(f'Creating table with SQL query: {x}')
        cur.execute(x)
    con.commit()


def test_get_random_resources(resource_ranges: ResourceRanges | None = None
                                ) -> SQLTableDict:
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


class DatabaseManager:
    def __init__(self, path: str) -> None:
        self.__path: str = path
        self.__con: sqlite3.Connection = sqlite3.connect(path)
        self.__cur: sqlite3.Cursor = self.__con.cursor()


    def commit(self) -> None:
        try:
            self.__con.commit()
        except sqlite3.Error:
            logger.debug('Cannot commit: not connected to a database.')


    def open(self) -> None:
        self.__con = sqlite3.connect(self.__path)
        self.__cur = self.__con.cursor()


    def close(self) -> None:
        # uncommitted transactions will be lost
        self.__con.close()
            

    def __del__(self):
        self.__con.close()


    @property
    def is_connected(self) -> bool:
        return all([self.__con, self.__cur])
    

    def get_table(self, table_name: str) -> list[SQLTableDict]:
        cursor = self.__cur.execute(f'SELECT * FROM {table_name} ;', {'dictionary': 'value'})
        table_rows: list[SQLTableDict] = []
        columns = [c[0] for c in cursor.description]
        for row in cursor.fetchall():
            table_rows.append(dict(zip(columns, row)))
        return table_rows


    def execute(self, query: str, dictionary: SQLTableDict, operation: str | None = None) -> None:
        operation = operation or 'UNSPECIFIED'
        if not self.is_connected:
            logger.debug('Cannot execute: not connected to a database.')
            return
        try:
            assert self.__cur
            self.__cur.execute(query, dictionary)
            logger.debug(f"Database {operation} operation successfully added to next commit.")

        except sqlite3.Error as e:
            logger.debug(f'Database {operation} operation failed: {e}')
            raise e


    def insert_table_from_dict(self, table_name: str, dictionary: SQLTableDict) -> None:
        keys, keyrefs = SQL_keyrefs(dictionary)
        query = f'INSERT INTO {table_name}({keys}) VALUES ({keyrefs}); '
        self.execute(query, dictionary, 'INSERT')


    def update_table_from_dict(self, table_name: str, primary_key: str, dictionary: SQLTableDict) -> None:
        primary_value = dictionary[primary_key]
        values = ', '.join([f'{k}=:{k}' for k in dictionary])
        query = f'UPDATE {table_name} SET {values} WHERE {primary_key} = "{primary_value}"; '
        self.execute(query, dictionary, 'UPDATE')


    def create_table_from_dict(self, 
                               table_name: str, 
                               primary_key: str, 
                               dictionary: dict[str, ImmutableType], 
                               foreign_keys: list[dict[str, str]] | None = None
                               ) -> None:
        
        maps = """
                CREATE TABLE IF NOT EXISTS maps
                (
                map_uuid TEXT PRIMARY KEY NOT NULL, 
                user_uuid TEXT NOT NULL,
                last_updated TEXT NOT NULL,
                current_turn INT NOT NULL,
                current_state TEXT NOT NULL,
                FOREIGN KEY(user_uuid) REFERENCES user_uuids(user_uuid)
                );
                
                """


    def new_map(self,
                user_uuid: str,
                width: int,
                height: int,
                # resource_ranges: dict[str, tuple[int, int]]
                ) -> None:
      
        logger.debug('Checking valid user UUID.')
        columns = self.get_table('user_uuids')
        uuids = [row['user_uuid'] for row in columns]
        if not user_uuid in uuids:
            raise ValueError('Unknown user UUID.')

        map_uuid: str = str(uuid4())
        tile_uuid: str

        logger.debug('Creating new map id for user')
        self.insert_table_from_dict('maps', {'map_uuid': map_uuid,
                                             'user_uuid': user_uuid})

        for x in range(1, width + 1):
            for y in range(1, height + 1):

                logger.debug(f'Generating tile details for coordinates {x, y}')
                tile_uuid = str(uuid4())

                logger.debug(f'Creating random resource profile for tile {tile_uuid}...')
                resources: SQLTableDict = test_get_random_resources()
                assert isinstance(resources, dict)

               
                resources.update({'tile_uuid': tile_uuid})
                tile = {'tile_uuid': tile_uuid,
                        'map_uuid': map_uuid,
                        'x': x,
                        'y': y,
                        # 'resource_multiplier': 2,
                        # 'movement_multiplier': 2,
                        # 'occupier_uuid': None,
                        # 'is_mountain': False,
                        # 'is_water': False
                        }
                
                logger.debug('Writing tile to database')
                try:
                    self.insert_table_from_dict('tiles', tile)
                except sqlite3.Error as e:
                    logger.debug(e)

                logger.debug(f'Writing tile resources to database {resources}')
                try:
                    self.insert_table_from_dict('resources', resources)
                except sqlite3.Error as e:
                    logger.debug(e)

        logger.debug('Committing database transaction.')
        self.commit()


def test_setup(w: int, h: int): 
    setup_database(TEST_DATABASE)

    b = DatabaseManager(TEST_DATABASE)
    b.insert_table_from_dict('user_uuids', {'user_uuid': 'TEST_USER_001'})
    b.new_map('TEST_USER_001', w, h)



def SQL_keyrefs(dictionary: SQLTableDict) -> tuple[str, str]:
    '''
    Turn a dictionary into a pair of strings representing the columns of an 
    SQL query. One is the column names 'key, key, key', the other is a 
    reference to the column names ':key, :key, :key'

    Examples
    --------
    >>> table_name = 'Demo'
    >>> dictionary = {"key1": val1, "key2": val2, "key3":val3}
    >>> keys, references = SQL_kv(dictionary)
    >>> query = f'INSERT INTO {table_name}({keys}) VALUES ({references}); '
    >>> print(query)
    INSERT INTO Demo(key1, key2, key3) VALUES (:key1, :key2, :key3);
    '''
    keys = ', '.join([k for k in dictionary])
    references = ', '.join([':'+ k for k in dictionary])
    return (keys, references)
