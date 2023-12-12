from typing import Mapping, MutableMapping


IntPair = tuple[int, int]
Coords = IntPair
ImmutableType = int | float | str | bool | None
SQLTableDict = MutableMapping[str, ImmutableType]
ResourceRanges = MutableMapping[str, IntPair]