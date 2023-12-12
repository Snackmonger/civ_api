from datetime import datetime
from typing import Optional
from uuid import uuid4

from sqlalchemy import Engine, select
from sqlalchemy.orm import Session

from src.civ_api.type_aliasing import IntPair
from src.civ_api.functions import test_get_random_resources
from databases.sqlalchemy_models import User, Tile, Resource


resource_generator = test_get_random_resources


class Alchemist:

    def __init__(self, engine: Engine) -> None:
        self.engine = engine
        self.session = Session(engine)


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
        
        # Create map for user id
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
        stmt = select(User).where(User.user_uuid == user_uuid)
        result = self.session.execute(stmt).scalars()
        return result.one()



    def get_tiles(self,
                user_uuid: str, 
                tiles: list[str]
                ) -> list[tuple[Tile, Resource]]:
        '''
        Get a list of tiles from a list of tile uuid addresses.
        '''
        tile_resources: list[tuple[Tile, Resource]] = []
        for uuid in tiles:
            stmt = select(Tile).where((Tile.tile_uuid==uuid) &
                                        (Tile.user_uuid == user_uuid)
                                        )
            result = self.session.execute(stmt).scalars()
            t = result.one()

            stmt = select(Resource).where(Resource.tile_uuid == uuid)
            result = self.session.execute(stmt).scalars()
            r = result.one()

            tile_resources.append((t, r))
        return tile_resources
        
