from datetime import datetime
from typing import Optional
from uuid import uuid4

from sqlalchemy import Engine, select, create_engine
from sqlalchemy.orm import Session

from src.civ_api.type_aliasing import IntPair
from src.civ_api.functions import test_get_random_resources
from databases.sqlalchemy_models import User, Tile, Resource


resource_generator = test_get_random_resources


class Alchemist:

    def __init__(self, db_address: str) -> None:

        self.engine = create_engine(db_address)
        self.session = Session(self.engine)


    def new_user(self, 
                 user_uuid: str, 
                 dimensions: Optional[IntPair] = None
                ) -> None:
        
        width, height = dimensions or (25, 25)
        self.session.add(User(user_uuid=user_uuid, 
                              last_updated=datetime.now(),
                              created=datetime.now(),
                              width=width,
                              height=height))
        
        # Create tile map
        for x in range(width):
            for y in range(height):
                tile_uuid = str(uuid4())
                self.session.add(Tile(user_uuid=user_uuid,
                                      tile_uuid=tile_uuid,
                                      x=x,
                                      y=y))

                self.session.add(Resource(**resource_generator(),
                                          tile_uuid=tile_uuid))


    def get_user(self, user_uuid: str) -> User:
        sql = select(User).where(User.user_uuid == user_uuid)
        result = self.session.execute(sql).scalars()
        return result.one()


    def get_tiles(self,
                user_uuid: str, 
                tile_uuids: list[str]
                ) -> list[tuple[Tile, Resource]]:
        '''
        Get a list of tiles from a list of tile uuid addresses.
        '''
        tile_resources: list[tuple[Tile, Resource]] = []
        for tile_uuid in tile_uuids:
            sql = select(Tile).where((Tile.tile_uuid==tile_uuid) &
                                     (Tile.user_uuid == user_uuid))
            result = self.session.execute(sql).scalars()
            t = result.one()

            sql = select(Resource).where(Resource.tile_uuid == tile_uuid)
            result = self.session.execute(sql).scalars()
            r = result.one()

            tile_resources.append((t, r))
        return tile_resources
    

    
        
