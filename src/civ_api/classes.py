from dataclasses import dataclass
from typing import TYPE_CHECKING

from .constants.enums import DiplomaticStatus


if TYPE_CHECKING:
    from typing import Optional
    from .entities import Unit
    from .constants.enums import UnitMoveTypes


@dataclass
class Coords:
    x: int
    y: int


class Move:
    '''Instructions for a unit to follow.'''

    def __init__(self) -> None:
        self.directive: UnitMoveTypes
        self.location: tuple[int, int]
        self.deferral: Optional[Move] = None
        self.target: Optional[Unit] = None


class DiplomaticRelations:

    def __init__(self):
        self.relation_table: dict[str, dict[str, str | int | float]]

    def are_hostile(self, player_1: str, player_2: str):
        return self.relation_table[player_1][player_2] == str(DiplomaticStatus.ENEMY)
    
    def are_allied(self, player_1: str, player_2: str):
        return self.relation_table[player_1][player_2] == str(DiplomaticStatus.ALLY)

