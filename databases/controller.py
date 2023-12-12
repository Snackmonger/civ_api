import sqlite3
from loguru import logger
from typing import Any
from civ_api.functions import SQL_keyrefs_eq, SQL_keyrefs_insert

from src.civ_api.type_aliasing import SQLTableDict, ImmutableType


class DatabaseManager:
    def __init__(self, path: str, user_uuid: str) -> None:
        self.__user_uuid: str = user_uuid
        self.__path: str = path
        self.__con: sqlite3.Connection = sqlite3.connect(path)
        self.__cur: sqlite3.Cursor = self.__con.cursor()

    def commit(self) -> None:
        try:
            self.__con.commit()
        except sqlite3.Error as e:
            logger.debug(f'Cannot commit: {e}.')

    def __del__(self):
        self.__con.close()

    
    def get_full_table(self, table_name: str) -> list[SQLTableDict]:
        cursor = self.__cur.execute(f'SELECT * FROM {table_name} ;')
        columns = [c[0] for c in cursor.description]
        rows = cursor.fetchall()
        return self.extract_to_dictionaries(columns, rows)
    

    def get_filtered_table(self, 
                           table_name: str, 
                           dictionary: dict[str, ImmutableType]
                           ) -> list[SQLTableDict]:
        symbols = SQL_keyrefs_eq(dictionary)
        conditions = "AND ".join(symbols)
        cursor = self.__cur.execute(f'SELECT * FROM {table_name} WHERE {conditions};', dictionary)
        columns = [c[0] for c in cursor.description]
        rows = cursor.fetchall()
        return self.extract_to_dictionaries(columns, rows)
    

    @staticmethod
    def extract_to_dictionaries(columns: list[str], rows: list[Any]) -> list[SQLTableDict]:
        table_rows: list[SQLTableDict] = []
        for row in rows:
            table_rows.append(dict(zip(columns, row)))
        return table_rows



    def execute(self, query: str, dictionary: SQLTableDict, operation: str | None = None) -> None:
        operation = operation or 'UNSPECIFIED'
        try:
            self.__cur.execute(query, dictionary)
            logger.debug(f"Database {operation} operation successfully added to next commit.")

        except sqlite3.Error as e:
            logger.debug(f'Database {operation} operation failed: {e}')
            raise e


    def insert_table_from_dict(self, table_name: str, dictionary: SQLTableDict) -> None:
        keys, keyrefs = SQL_keyrefs_insert(dictionary)
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
        columns = self.get_full_table('user_uuids')
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

