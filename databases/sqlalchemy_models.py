import datetime
from typing import (Callable,
                    Optional,
                    Any)

from sqlalchemy import (create_engine,
                        ForeignKey)

from sqlalchemy.orm import (DeclarativeBase,
                            Mapped,
                            mapped_column,
                            relationship)

from src.civ_api.constants.enums import GamePhases


engine = create_engine("sqlite:///databases/learn_sqlalchemy.db",
                       echo=True)

# NOTE: We can use vars() to get the attributes of the class/instance. It 
# will add _sa_instance_state

# returned = {'_sa_instance_state': <sqlalchemy.orm.state.InstanceState object at 0x000002009DED2ED0>, 
#             'current_turn': None, 
#             'current_state': None, 
#             'created': datetime.datetime(2023, 12, 11, 23, 25, 17, 271830), 
#             'user_uuid': 'TEST_USER_001', 
#             'last_updated': datetime.datetime(2023, 12, 11, 23, 25, 17, 271830)}



class Base(DeclarativeBase):
    ...


class User(Base):
    __tablename__ = "user"

    user_uuid: Mapped[str] = mapped_column(primary_key=True)

    created: Mapped[datetime.datetime]
    last_updated: Mapped[Optional[datetime.datetime]]
    width: Mapped[int]
    height: Mapped[int]
    current_turn: Mapped[Optional[int]]
    current_state: Mapped[Optional[GamePhases]]
    
    tiles: Mapped[list["Tile"]] = relationship(back_populates='parent')



class Tile(Base):
    __tablename__ = "tile"

    tile_uuid: Mapped[str] = mapped_column(primary_key=True)
    user_uuid: Mapped[str] = mapped_column(ForeignKey("user.user_uuid"))

    x: Mapped[int]
    y: Mapped[int]
    parent: Mapped["User"] = relationship(back_populates='tiles')
    resources: Mapped["Resource"] = relationship(back_populates="tile")

    def __repr__(self) -> str:
        return f'Tile {self.tile_uuid} @ ({self.x}, {self.y})'



class Resource(Base):
    __tablename__ = "resource"

    tile_uuid:  Mapped[str] = mapped_column(ForeignKey("tile.tile_uuid"),
                                            primary_key=True)
    tile: Mapped["Tile"] = relationship(back_populates='resources')

    wheat:      Mapped[Optional[int]]
    water:      Mapped[Optional[int]]
    stone:      Mapped[Optional[int]]
    marble:     Mapped[Optional[int]]
    iron:       Mapped[Optional[int]]
    coal:       Mapped[Optional[int]]
    gems:       Mapped[Optional[int]]
    horses:     Mapped[Optional[int]]
    cattle:     Mapped[Optional[int]]
    sheep:      Mapped[Optional[int]]
    fish:       Mapped[Optional[int]]
    pearls:     Mapped[Optional[int]]
    wild_game:  Mapped[Optional[int]]
    sugar:      Mapped[Optional[int]]
    farming:    Mapped[Optional[int]]
    salt:       Mapped[Optional[int]]
    gold:       Mapped[Optional[int]]
    silver:     Mapped[Optional[int]]
    wood:       Mapped[Optional[int]]
    clay:       Mapped[Optional[int]]
    olives:     Mapped[Optional[int]]
    grapes:     Mapped[Optional[int]]
    fruit:      Mapped[Optional[int]]
    ivory:      Mapped[Optional[int]]
    silk:       Mapped[Optional[int]]
    spices:     Mapped[Optional[int]]
    dyes:       Mapped[Optional[int]]
    incense:    Mapped[Optional[int]]


    def __repr__(self) -> str:
        expr = ''
        for k, v in self.total.items():
            expr += k + ': ' + str(v) + ', '
        expr = expr.strip(', ')
        return f'Resource @ tile {self.tile_uuid} :: {expr}'
    

    @property
    def total(self) -> dict[str, int]:
        '''
        Get a dictionary of the resources that are not None.
        '''
        skip = ['_sa_instance_state', 'tile_uuid']
        r: dict[str, int] = {}
        for k, v in vars(self):
            if not k in skip and v:
                assert isinstance(v, int)
                r.update({k:v})
        return r


