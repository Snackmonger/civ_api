from sqlalchemy import (CheckConstraint, 
                        create_engine, 
                        Table, 
                        Column, 
                        Integer, 
                        String, 
                        ForeignKey)

from sqlalchemy.orm import (DeclarativeBase,
                            Mapped,
                            mapped_column,
                            relationship)



class Base(DeclarativeBase):
    ...


class Tile(Base):
    __tablename__ = "tiles"
    tile_uuid: Mapped[str] = mapped_column(primary_key=True)
    map_uuid: Mapped[str]
    x: Mapped[int]
    y: Mapped[int]