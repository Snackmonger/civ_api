from typing import Mapping


IntPair = tuple[int, int]
Coords = IntPair
ImmutableType = int | float | str | bool | None
SQLTableDict = Mapping[str, ImmutableType]
ResourceRanges = Mapping[str, IntPair]